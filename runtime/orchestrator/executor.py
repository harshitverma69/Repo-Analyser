"""Deterministic skill execution — golden replay, no LLM."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, cast

from runtime.deterministic import DETERMINISTIC_STAMP, canonical_json_dumps, strip_volatile_keys
from runtime.models import RunContext, SkillResult
from runtime.orchestrator.planner import ExecutionPlan, discover_skills, load_registry
from runtime.orchestrator.result_aggregator import aggregate_results, display_path, report_to_runner_summary
from runtime.skill_parser import SkillDefinition, task_sort_key, validate_output_schema

ROOT = Path(__file__).resolve().parent.parent.parent
GOLDEN_DIR = ROOT / "generated_projects" / "_golden"
GENERATED_ROOT = ROOT / "generated_projects"
CORE_REGISTRY_PATH = ROOT / "core" / "skill_registry.json"

DEFAULT_RUN_INPUTS = {
    "repository_path": str(ROOT),
    "task_description": "repo-analyser-deterministic-run",
    "lanes": 2,
    "module_path": ".",
    "output_dir": str(ROOT / "generated_projects"),
    "service_path": str(ROOT),
    "project_name": "repo-analyser-demo-project",
    "mode": "api",
    "entry_point_id": "GET:/health",
    "service_port": 8080,
    "ci_platform": "github_actions",
    "bootstrap_type": "makefile_mise",
    "cluster": "kind",
    "provider": "aws",
    "resources": ["s3", "ec2"],
    "benchmark_target": "GET /health",
    "diff_or_pr_ref": "HEAD~1",
    "change_spec": {"description": "deterministic change", "target_module": "app"},
    "bug_context": {"symptoms": "none", "reproduction_hint": "n/a"},
}


class SkillExecutor:
    """Execute skills deterministically against golden reference outputs."""

    def __init__(self, context: RunContext, registry: dict | None = None):
        self.context = context
        self.registry = registry or load_registry(context.registry_path)
        self.execution_log: list[dict] = []

    def _artifact_input_available(self, key: str, skill: SkillDefinition) -> bool:
        if key in self.context.inputs:
            return True
        if not key.endswith(".json"):
            return False
        for dep in sorted(skill.depends_on, key=task_sort_key):
            dep_meta = self.registry.get("skills", {}).get(dep, {})
            if dep_meta.get("output_file") == key:
                return (self.context.run_dir / dep / "output.json").is_file()
        return False

    def validate_inputs(self, skill: SkillDefinition) -> list[str]:
        errors: list[str] = []
        contract = skill.input_contract or {}

        for key in sorted(contract):
            if key.endswith(".json"):
                if not self._artifact_input_available(key, skill):
                    errors.append(f"MISSING_INPUT: {key}")
                continue
            if key not in self.context.inputs:
                errors.append(f"MISSING_INPUT: {key}")

        repository_path = self.context.inputs.get("repository_path")
        if "repository_path" in contract and repository_path:
            if not Path(str(repository_path)).exists():
                errors.append("INPUT_CONTRACT_VIOLATION: repository_path not found")

        for dep in sorted(skill.depends_on, key=task_sort_key):
            dep_output = self.context.run_dir / dep / "output.json"
            if not dep_output.is_file():
                errors.append(f"MISSING_DEPENDENCY_OUTPUT: {dep}")

        return sorted(errors)

    def load_golden_output(self, skill_id: str) -> dict[str, Any]:
        meta = self.registry["skills"][skill_id]
        golden_path = self.context.golden_dir / skill_id / meta["output_file"]
        if not golden_path.is_file():
            raise FileNotFoundError(f"Golden output missing: {golden_path}")
        return cast(dict[str, Any], json.loads(golden_path.read_text(encoding="utf-8")))

    def normalize_output(self, output: dict, skill_id: str) -> dict:
        normalized = strip_volatile_keys(dict(output))
        normalized["task_id"] = skill_id
        return normalized

    def execute_steps(self, skill: SkillDefinition, skill_id: str) -> tuple[dict, list[str], list[str]]:
        steps_executed: list[str] = []
        errors: list[str] = []

        steps_executed.append("validate_input_contract")
        input_errors = self.validate_inputs(skill)
        if input_errors:
            return {}, steps_executed, input_errors

        steps_executed.append("load_golden_reference_output")
        try:
            output = self.load_golden_output(skill_id)
        except FileNotFoundError as exc:
            return {}, steps_executed, [str(exc)]

        steps_executed.append("normalize_output")
        output = self.normalize_output(output, skill_id)

        steps_executed.append("validate_output_contract")
        schema_errors = validate_output_schema(output, skill.output_contract)
        if schema_errors:
            errors.extend(schema_errors)

        for step in skill.execution_steps:
            steps_executed.append(f"record_step:{step[:80]}")

        return output, steps_executed, errors

    def run_skill(self, skill: SkillDefinition) -> SkillResult:
        stamp = DETERMINISTIC_STAMP
        skill_id = skill.skill_id
        out_dir = self.context.run_dir / skill_id
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / "output.json"

        output, steps, errors = self.execute_steps(skill, skill_id)
        status = "complete" if output and not errors else "failed"

        if status == "complete":
            output_path.write_text(canonical_json_dumps(output), encoding="utf-8")
            from runtime.skill_finish import export_markdown_reports, show_skill_report

            export_markdown_reports(self.context.run_dir, out_dir)
            if os.environ.get("REPO_ANALYSER_AUTO_SKILL_DONE", "1") != "0":
                show_skill_report(self.context.run_dir, skill_id, save_md=False)

        result = SkillResult(
            skill_id=skill_id,
            status=status,
            output_path=display_path(output_path),
            started_at=stamp,
            completed_at=stamp,
            steps_executed=steps,
            errors=errors,
        )
        self.execution_log.append(result.to_dict())
        return result

    def run_plan(self, plan: ExecutionPlan) -> dict:
        self.context.run_dir.mkdir(parents=True, exist_ok=True)
        results: list[SkillResult] = []

        for wave_index, wave in enumerate(plan.parallel_waves):
            for skill_id in wave:
                skill = plan.skills.get(skill_id)
                if skill is None:
                    skills = discover_skills()
                    skill = skills[skill_id]

                results.append(self.run_skill(skill))
                if results[-1].status != "complete" and not self.context.continue_on_failure:
                    report = aggregate_results(plan, results, self.context.run_dir, wave_index, aborted=True)
                    return report_to_runner_summary(report)

        aborted = any(result.status != "complete" for result in results)
        report = aggregate_results(
            plan,
            results,
            self.context.run_dir,
            len(plan.parallel_waves) - 1,
            aborted=aborted,
        )
        return report_to_runner_summary(report)

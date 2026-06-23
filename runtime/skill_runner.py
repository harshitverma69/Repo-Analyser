"""Deterministic skill executor — backward-compatible public API."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from runtime.deterministic import DETERMINISTIC_STAMP, canonical_json_dumps
from runtime.models import RunContext, SkillResult
from runtime.orchestrator.executor import DEFAULT_RUN_INPUTS, SkillExecutor
from runtime.orchestrator.planner import ExecutionPlan, discover_skills
from runtime.orchestrator.result_aggregator import aggregate_results, display_path, report_to_runner_summary
from runtime.skill_parser import SkillDefinition, validate_output_schema

ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = ROOT / "generated_projects" / "_golden"
GENERATED_ROOT = ROOT / "generated_projects"
CORE_REGISTRY_PATH = ROOT / "core" / "skill_registry.json"


@dataclass
class SkillRunResult:
    """Legacy result type — prefer runtime.models.SkillResult."""

    skill_id: str
    status: str
    output_path: str
    started_at: str
    completed_at: str
    steps_executed: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return SkillResult(
            skill_id=self.skill_id,
            status=self.status,
            output_path=self.output_path,
            started_at=self.started_at,
            completed_at=self.completed_at,
            steps_executed=self.steps_executed,
            errors=self.errors,
        ).to_dict()


class SkillRunner:
    """Backward-compatible wrapper around SkillExecutor."""

    def __init__(
        self,
        run_id: str,
        run_dir: Path | None = None,
        golden_dir: Path | None = None,
        registry_path: Path | None = None,
        inputs: dict | None = None,
        continue_on_failure: bool = True,
    ):
        self.run_id = run_id
        self.run_dir = run_dir or (GENERATED_ROOT / run_id)
        self.golden_dir = golden_dir or GOLDEN_DIR
        self.registry_path = registry_path or CORE_REGISTRY_PATH
        self.inputs = {**DEFAULT_RUN_INPUTS, **(inputs or {})}
        self.continue_on_failure = continue_on_failure
        self.context = RunContext(
            run_id=run_id,
            run_dir=self.run_dir,
            golden_dir=self.golden_dir,
            registry_path=self.registry_path,
            inputs=self.inputs,
            continue_on_failure=continue_on_failure,
        )
        self._executor = SkillExecutor(self.context)
        self.registry = self._executor.registry
        self.execution_log: list[dict] = []

    def _artifact_input_available(self, key: str, skill: SkillDefinition) -> bool:
        return self._executor._artifact_input_available(key, skill)

    def validate_inputs(self, skill):
        return self._executor.validate_inputs(skill)

    def load_golden_output(self, skill_id: str) -> dict:
        return self._executor.load_golden_output(skill_id)

    def normalize_output(self, output: dict, skill_id: str) -> dict:
        return self._executor.normalize_output(output, skill_id)

    def execute_steps(self, skill, skill_id: str):
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

    def run_skill(self, skill) -> SkillRunResult:
        stamp = DETERMINISTIC_STAMP
        skill_id = skill.skill_id
        out_dir = self.run_dir / skill_id
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / "output.json"

        output, steps, errors = self.execute_steps(skill, skill_id)
        status = "complete" if output and not errors else "failed"

        if status == "complete":
            output_path.write_text(canonical_json_dumps(output), encoding="utf-8")
            from runtime.skill_finish import export_markdown_reports, show_skill_report

            export_markdown_reports(self.run_dir, out_dir)
            if os.environ.get("REPO_ANALYSER_AUTO_SKILL_DONE", "1") != "0":
                show_skill_report(self.run_dir, skill_id, save_md=False)

        result = SkillRunResult(
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
        self.run_dir.mkdir(parents=True, exist_ok=True)
        results: list[SkillResult] = []

        for wave_index, wave in enumerate(plan.parallel_waves):
            for skill_id in wave:
                skill = plan.skills.get(skill_id)
                if skill is None:
                    skills = discover_skills()
                    skill = skills[skill_id]

                legacy = self.run_skill(skill)
                results.append(
                    SkillResult(
                        skill_id=legacy.skill_id,
                        status=legacy.status,
                        output_path=legacy.output_path,
                        started_at=legacy.started_at,
                        completed_at=legacy.completed_at,
                        steps_executed=legacy.steps_executed,
                        errors=legacy.errors,
                    )
                )
                if results[-1].status != "complete" and not self.continue_on_failure:
                    report = aggregate_results(plan, results, self.run_dir, wave_index, aborted=True)
                    return report_to_runner_summary(report)

        aborted = any(result.status != "complete" for result in results)
        report = aggregate_results(
            plan,
            results,
            self.run_dir,
            len(plan.parallel_waves) - 1,
            aborted=aborted,
        )
        return report_to_runner_summary(report)


def main(argv: list[str] | None = None) -> int:
    import argparse

    from runtime.deterministic import canonical_json_dumps
    from runtime.orchestrator import SkillOrchestrator

    parser = argparse.ArgumentParser(description="Repo-Analyser deterministic skill runner")
    parser.add_argument("--run-id", default="pipeline-run")
    parser.add_argument("--skill", help="Single skill ID, e.g. B1")
    parser.add_argument("--domain", choices=["B", "I", "A", "D"], help="Run all skills in domain")
    parser.add_argument("--full-pipeline", action="store_true", help="Run all 24 skills in DAG order")
    parser.add_argument("--repository-path", default=str(ROOT))
    parser.add_argument("--plan-only", action="store_true", help="Print execution plan only")
    args = parser.parse_args(argv)

    orchestrator = SkillOrchestrator()
    orchestrator.load_registry()
    orchestrator.discover_skills()

    if args.full_pipeline:
        plan = orchestrator.build_plan(args.run_id, full_pipeline=True)
    elif args.domain:
        plan = orchestrator.build_plan(args.run_id, domain=args.domain)
    elif args.skill:
        plan = orchestrator.build_plan(args.run_id, skill_ids=[args.skill.upper()])
    else:
        print("Provide --skill, --domain, or --full-pipeline", file=sys.stderr)
        return 1

    if args.plan_only:
        print(canonical_json_dumps(plan.to_dict()).rstrip())
        return 0

    runner = SkillRunner(
        run_id=args.run_id,
        inputs={"repository_path": args.repository_path},
    )
    summary = runner.run_plan(plan)
    print(canonical_json_dumps(summary).rstrip())
    return 0 if summary["status"] == "complete" else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

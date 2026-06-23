"""Coverage for orchestrator executor and CLI modules."""

from __future__ import annotations

from pathlib import Path

import pytest
from runtime.models import RunContext
from runtime.orchestrator import SkillOrchestrator
from runtime.orchestrator.cli import main as orchestrator_cli_main
from runtime.orchestrator.executor import DEFAULT_RUN_INPUTS, SkillExecutor

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def orchestrator() -> SkillOrchestrator:
    orch = SkillOrchestrator(
        skills_root=ROOT / "skills",
        registry_path=ROOT / "core" / "skill_registry.json",
    )
    orch.load_registry()
    orch.discover_skills()
    return orch


def test_skill_executor_runs_b1(tmp_path: Path, orchestrator: SkillOrchestrator):
    run_dir = tmp_path / "exec-run"
    context = RunContext(
        run_id="exec-run",
        run_dir=run_dir,
        golden_dir=ROOT / "generated_projects" / "_golden",
        registry_path=ROOT / "core" / "skill_registry.json",
        inputs={**DEFAULT_RUN_INPUTS, "repository_path": str(ROOT)},
    )
    executor = SkillExecutor(context)
    result = executor.run_skill(orchestrator.get_skill("B1"))
    assert result.status == "complete"
    assert (run_dir / "B1" / "output.json").is_file()


def test_skill_executor_run_plan(tmp_path: Path, orchestrator: SkillOrchestrator):
    run_id = "exec-plan"
    run_dir = tmp_path / run_id
    context = RunContext(
        run_id=run_id,
        run_dir=run_dir,
        golden_dir=ROOT / "generated_projects" / "_golden",
        registry_path=ROOT / "core" / "skill_registry.json",
        inputs={"repository_path": str(ROOT)},
    )
    plan = orchestrator.build_plan(run_id, skill_ids=["B1", "B2"])
    summary = SkillExecutor(context).run_plan(plan)
    assert summary["status"] == "complete"
    assert summary["completed"] == ["B1", "B2"]


def test_orchestrator_cli_validate_dag(capsys):
    rc = orchestrator_cli_main(["--validate-dag"])
    assert rc == 0
    assert "VALID" in capsys.readouterr().out

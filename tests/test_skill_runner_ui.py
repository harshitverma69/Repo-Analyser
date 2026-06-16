"""Tests for skill_runner auto UI hook."""

from __future__ import annotations

import json
from pathlib import Path

from runtime.skill_orchestrator import SkillOrchestrator
from runtime.skill_runner import SkillRunner


ROOT = Path(__file__).resolve().parent.parent


def test_run_skill_auto_displays_ui(tmp_path: Path, capsys, monkeypatch):
    monkeypatch.setenv("CACOS_AUTO_SKILL_DONE", "1")
    run_id = "ui-hook-test"
    runner = SkillRunner(
        run_id=run_id,
        run_dir=tmp_path / run_id,
        golden_dir=ROOT / "generated_projects" / "_golden",
        registry_path=ROOT / "core" / "skill_registry.json",
        inputs={"repository_path": str(ROOT)},
    )
    orch = SkillOrchestrator(
        skills_root=ROOT / "skills",
        registry_path=ROOT / "core" / "skill_registry.json",
    )
    orch.discover_skills()
    result = runner.run_skill(orch.get_skill("B1"))
    assert result.status == "complete"
    out = capsys.readouterr().out
    assert "INVENTORY" in out or "Repo Artifact Inventory" in out


def test_run_skill_ui_disabled(tmp_path: Path, capsys, monkeypatch):
    monkeypatch.setenv("CACOS_AUTO_SKILL_DONE", "0")
    run_id = "ui-hook-off"
    runner = SkillRunner(
        run_id=run_id,
        run_dir=tmp_path / run_id,
        golden_dir=ROOT / "generated_projects" / "_golden",
        registry_path=ROOT / "core" / "skill_registry.json",
        inputs={"repository_path": str(ROOT)},
    )
    orch = SkillOrchestrator(
        skills_root=ROOT / "skills",
        registry_path=ROOT / "core" / "skill_registry.json",
    )
    orch.discover_skills()
    result = runner.run_skill(orch.get_skill("B1"))
    assert result.status == "complete"
    assert capsys.readouterr().out == ""
    assert json.loads((tmp_path / run_id / "B1" / "output.json").read_text(encoding="utf-8"))

"""Tests for typed domain models."""

from __future__ import annotations

from pathlib import Path

from runtime.models import ExecutionReport, RunContext, SkillResult, SkillSpec


def test_skill_spec_from_registry_entry():
    spec = SkillSpec.from_registry_entry(
        "B1",
        {
            "name": "Repo Inventory",
            "level": "BASIC",
            "level_code": "B",
            "depends_on": [],
            "output_file": "output.json",
        },
    )
    assert spec.skill_id == "B1"
    assert spec.level_code == "B"
    assert spec.depends_on == []


def test_skill_result_to_dict_sorted_errors():
    result = SkillResult(
        skill_id="B1",
        status="failed",
        output_path="out.json",
        started_at="t0",
        completed_at="t1",
        errors=["Z", "A"],
    )
    payload = result.to_dict()
    assert payload["errors"] == ["A", "Z"]


def test_execution_report_to_dict():
    report = ExecutionReport(
        run_id="run-1",
        status="complete",
        completed=["B1"],
        failed=[],
        total_skills=1,
    )
    payload = report.to_dict()
    assert payload["completed_count"] == 1
    assert payload["failed_count"] == 0


def test_run_context_repository_path():
    ctx = RunContext(
        run_id="r",
        run_dir=Path("/tmp/r"),
        golden_dir=Path("/tmp/g"),
        registry_path=Path("/tmp/reg.json"),
        inputs={"repository_path": "/repo"},
    )
    assert ctx.repository_path == "/repo"

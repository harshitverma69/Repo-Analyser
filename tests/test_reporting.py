"""Tests for reporting helpers."""

from __future__ import annotations

import json
from pathlib import Path

from runtime.deterministic import canonical_json_dumps
from runtime.reporting import ReportMetadata
from runtime.reporting import canonical_json_dumps as reporting_dumps
from runtime.reporting.json_writer import write_json
from runtime.reporting.markdown_writer import export_skill_markdown
from runtime.reporting.renderer import render_report

ROOT = Path(__file__).resolve().parent.parent


def test_report_metadata_frozen():
    meta = ReportMetadata(run_id="r", skill_id="B1", task_id="B1", level="B")
    assert meta.skill_id == "B1"


def test_write_json_roundtrip(tmp_path: Path):
    path = write_json(tmp_path / "out.json", {"task_id": "B1", "artifacts": []})
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["task_id"] == "B1"


def test_reporting_reexports_match():
    assert reporting_dumps({"a": 1}).strip() == canonical_json_dumps({"a": 1}).strip()


def test_render_report_from_golden():
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    payload = json.loads(golden.read_text(encoding="utf-8"))
    report = render_report(payload, task_id="B1")
    assert "B1" in report


def test_export_skill_markdown(tmp_path: Path):
    skill_dir = tmp_path / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")
    path = export_skill_markdown(skill_dir)
    assert path.is_file()

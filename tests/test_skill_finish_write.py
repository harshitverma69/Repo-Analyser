"""Tests for write_skill_output auto UI hook."""

from __future__ import annotations

import json
from pathlib import Path

from runtime.skill_finish import finish_skill, main, write_skill_output

ROOT = Path(__file__).resolve().parent.parent


def test_write_skill_output_writes_and_displays(tmp_path: Path, capsys):
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    payload = json.loads(golden.read_text(encoding="utf-8"))

    path = write_skill_output("demo-run", "B1", payload, generated_root=tmp_path)
    assert path.is_file()
    assert (tmp_path / "demo-run" / "B1" / "output.md").is_file()
    out = capsys.readouterr().out
    assert "INVENTORY" in out or "Repo Artifact Inventory" in out


def test_write_skill_output_no_ui(tmp_path: Path, capsys):
    payload = {"task_id": "A5", "issues": [], "level": "A", "scan_complete": True, "warnings": []}
    write_skill_output("demo", "A5", payload, generated_root=tmp_path, show_ui=False)
    assert capsys.readouterr().out == ""
    assert (tmp_path / "demo" / "A5" / "output.json").is_file()
    assert (tmp_path / "demo" / "A5" / "output.md").is_file()


def test_main_write_subcommand(tmp_path: Path, capsys):
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(
        json.dumps({"task_id": "A5", "issues": [], "level": "A", "scan_complete": True}),
        encoding="utf-8",
    )
    runs = tmp_path / "runs"
    runs.mkdir()
    # Patch GENERATED_ROOT via env path - use finish on written file
    from runtime import skill_finish

    skill_finish.GENERATED_ROOT = runs
    rc = main(
        [
            "write",
            "--run-id",
            "review",
            "--skill",
            "A5",
            "--payload-file",
            str(payload_file),
        ]
    )
    assert rc == 0
    assert (runs / "review" / "A5" / "output.json").is_file()
    assert (runs / "review" / "A5" / "output.md").is_file()
    out = capsys.readouterr().out
    assert "CLEAN" in out or "REVIEWED" in out


def test_finish_skill_missing_run(tmp_path: Path, capsys):
    rc = finish_skill("missing", "B1", generated_root=tmp_path)
    assert rc == 1
    assert "not found" in capsys.readouterr().err.lower()

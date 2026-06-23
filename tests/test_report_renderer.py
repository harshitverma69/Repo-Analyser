"""Tests for Markdown report rendering."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime.report_renderer import export_run_markdown, export_skill_markdown, render_report
from runtime.report_ui import render_terminal_ui

ROOT = Path(__file__).resolve().parent.parent


def test_render_terminal_ui_a5():
    payload = json.loads(
        (ROOT / "generated_projects" / "_golden" / "A5" / "code_review_report.json").read_text(encoding="utf-8")
    )
    ui = render_terminal_ui("repo-analyser", "A5", payload)
    assert "Adversarial Code Review" in ui or "code-review" in ui
    assert "CLEAN" in ui or "REVIEWED" in ui or "NEEDS FIX" in ui


def test_compute_outcome_b1_golden():
    from runtime.report_ui import compute_outcome

    golden = json.loads(
        (ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json").read_text(encoding="utf-8")
    )
    label, tone, headline, metrics = compute_outcome("B1", golden)
    assert label == "INVENTORY OK"
    assert tone == "ok"
    assert "artifact" in headline.lower()


def test_render_b1_golden():
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    payload = json.loads(golden.read_text(encoding="utf-8"))
    md = render_report(payload, task_id="B1")
    assert "# B1 — Repo Artifact Inventory" in md
    assert "## Summary" in md
    assert "OrderService" in md


def test_export_master_mapping_run(tmp_path: Path):
    run_dir = tmp_path / "master-mapping"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    payload = {
        "task_id": "B1",
        "level": "B",
        "files_scanned": 2,
        "modules": [{"name": "com.example", "path": "src/main/java/com/example/"}],
        "artifacts": {
            "controllers": [{"name": "MasterMappingController", "file_path": "src/MasterMappingController.java"}],
            "classes": [],
            "interfaces": [],
            "services": [],
            "models": [],
            "repositories": [],
            "jobs": [],
            "consumers": [],
            "configurations": [],
            "utilities": [],
        },
        "dependency_graph_summary": {"nodes": ["com.example"], "edges": []},
        "limitations": [],
    }
    (skill_dir / "output.json").write_text(json.dumps(payload), encoding="utf-8")

    paths = export_run_markdown(run_dir)
    assert (run_dir / "REPORT.md").is_file()
    assert (run_dir / "B1" / "output.md").is_file()
    assert any(p.name == "output.md" for p in paths)

    md = (run_dir / "B1" / "output.md").read_text(encoding="utf-8")
    assert "MasterMappingController" in md
    assert "## Artifacts" in md


def test_render_a5_issues_markdown_fields():
    payload = {
        "task_id": "A5",
        "issues": [
            {
                "id": "ISS-1",
                "severity": "BLOCKING",
                "file_path": "app.py",
                "line": 42,
                "description": "Bug",
                "suggested_fix": "Fix it",
                "verification_steps": ["Run tests", "Check logs"],
            }
        ],
    }
    md = render_report(payload, task_id="A5")
    assert "Fix it" in md
    assert "Run tests" in md
    assert "42" in md


def test_render_a5_issues_shows_verification_steps():
    from runtime.report_ui import Theme, render_a5_issues

    issues = [
        {
            "id": "ISS-1",
            "severity": "blocking",
            "file_path": "app.py",
            "line": 1,
            "description": "bug",
            "suggested_fix": "fix it",
            "verification_steps": ["run pytest"],
        }
    ]
    lines = render_a5_issues(issues, Theme())
    text = "\n".join(lines)
    assert "fix it" in text
    assert "run pytest" in text


def test_finish_skill_missing_run(tmp_path: Path, capsys):
    from runtime.skill_finish import finish_skill

    rc = finish_skill("missing-run", "B1", generated_root=tmp_path)
    assert rc == 1
    assert "not found" in capsys.readouterr().err.lower()


def test_finish_skill_renders_b1(tmp_path: Path, capsys):
    from runtime.skill_finish import finish_skill

    run_dir = tmp_path / "demo"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "output.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")

    rc = finish_skill("demo", "B1", generated_root=tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "Repo Artifact Inventory" in out or "INVENTORY" in out


def test_cmd_clean_runs(tmp_path: Path, monkeypatch, capsys):
    from scripts import repo_analyser

    runs_root = tmp_path / "generated_projects"
    runs_root.mkdir()
    (runs_root / "_golden").mkdir()
    (runs_root / "ephemeral").mkdir()
    (runs_root / "ephemeral" / "B1").mkdir()
    (runs_root / "keep-me.txt").write_text("nope", encoding="utf-8")

    monkeypatch.setattr(repo_analyser, "ROOT", tmp_path)
    rc = repo_analyser.cmd_clean_runs(argparse.Namespace())
    assert rc == 0
    assert not (runs_root / "ephemeral").exists()
    assert (runs_root / "_golden").is_dir()
    assert "ephemeral" in capsys.readouterr().out


def test_export_skill_markdown(tmp_path: Path):
    skill_dir = tmp_path / "B1"
    skill_dir.mkdir()
    payload = {
        "task_id": "B1",
        "level": "B",
        "files_scanned": 1,
        "modules": [{"name": "app", "path": "app/"}],
        "artifacts": {
            "controllers": [{"name": "HealthController", "file_path": "app/Health.java"}],
            "classes": [],
            "interfaces": [],
            "services": [],
            "models": [],
            "repositories": [],
            "jobs": [],
            "consumers": [],
            "configurations": [],
            "utilities": [],
        },
        "dependency_graph_summary": {"nodes": ["app"], "edges": []},
        "limitations": [],
    }
    (skill_dir / "output.json").write_text(json.dumps(payload), encoding="utf-8")
    md_path = export_skill_markdown(skill_dir)
    assert md_path.name == "output.md"
    assert "HealthController" in md_path.read_text(encoding="utf-8")

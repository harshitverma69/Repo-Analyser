"""Full coverage for runtime.skill_finish and entry points."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from runtime.skill_finish import (
    _interactive_menu,
    export_markdown_reports,
    finish_skill,
    main,
    show_skill_report,
    write_skill_output,
)

ROOT = Path(__file__).resolve().parent.parent


def test_export_markdown_reports_failure(tmp_path, capsys):
    with patch("runtime.skill_finish.export_skill_markdown", side_effect=RuntimeError("boom")):
        export_markdown_reports(tmp_path, tmp_path / "B1")
    assert "Warning" in capsys.readouterr().err


def test_write_skill_output_frontend_sync_failure(tmp_path, capsys):
    payload = {"task_id": "A5", "issues": [], "level": "A", "scan_complete": True}
    with patch("runtime.frontend_sync.publish_skill_run", side_effect=RuntimeError("sync fail")):
        write_skill_output("demo", "A5", payload, generated_root=tmp_path, show_ui=False)
    assert "frontend sync failed" in capsys.readouterr().err.lower()


def test_show_skill_report_missing_output(tmp_path, capsys):
    rc = show_skill_report(tmp_path / "missing", "B1", sync_frontend=False)
    assert rc == 1
    assert "No output found" in capsys.readouterr().err


def test_show_skill_report_sync_failure(tmp_path, capsys):
    run_dir = tmp_path / "run"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")
    with patch("runtime.frontend_sync.publish_skill_run", side_effect=RuntimeError("x")):
        rc = show_skill_report(run_dir, "B1", save_md=False, sync_frontend=True)
    assert rc == 0
    assert "frontend sync failed" in capsys.readouterr().err.lower()


def test_interactive_menu_quit_and_refresh(tmp_path, monkeypatch, capsys):
    run_dir = tmp_path / "run"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")

    inputs = iter(["q"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    assert _interactive_menu(run_dir, "B1") == 0

    inputs = iter(["r", "q"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    monkeypatch.setattr(
        "runtime.skill_finish.show_skill_report",
        lambda *a, **k: 0,
    )
    assert _interactive_menu(run_dir, "B1") == 0


def test_interactive_menu_browse_and_submenu(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")

    monkeypatch.setattr("runtime.report_cli.interactive_loop", lambda _root: 0)
    monkeypatch.setattr("runtime.report_cli.list_skills", lambda _d: [("B1", skill_dir / "inventory_report.json")])

    inputs = iter(["b"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    assert _interactive_menu(run_dir, "B1") == 0

    inputs = iter(["", "1", "4", "q"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    assert _interactive_menu(run_dir, "B1") == 0

    inputs = iter(["", "2", "1", "4", "q"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    assert _interactive_menu(run_dir, "B1") == 0

    inputs = iter(["", "3"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    assert _interactive_menu(run_dir, "B1") == 0

    inputs = iter(["x", "q"])
    monkeypatch.setattr("builtins.input", lambda _=None: next(inputs))
    assert _interactive_menu(run_dir, "B1") == 0


def test_interactive_menu_submenu_eof(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")

    calls = {"n": 0}

    def eof_on_submenu(_=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return ""
        raise EOFError

    monkeypatch.setattr("builtins.input", eof_on_submenu)
    assert _interactive_menu(run_dir, "B1") == 0


def test_interactive_menu_eof(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")

    def eof(*_a, **_k):
        raise EOFError

    monkeypatch.setattr("builtins.input", eof)
    assert _interactive_menu(run_dir, "B1") == 0


def test_main_show_and_legacy(capsys, tmp_path):
    run_dir = tmp_path / "legacy"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "output.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")

    import runtime.skill_finish as mod

    mod.GENERATED_ROOT = tmp_path
    rc = main(["show", "--run-id", "legacy", "--skill", "B1", "--no-md"])
    assert rc == 0

    rc = main(["--run-id", "legacy", "--skill", "B1", "--no-md"])
    assert rc == 0


def test_main_missing_args(capsys):
    with pytest.raises(SystemExit):
        main([])


def test_skill_finish_module_main(tmp_path, monkeypatch):
    import runtime.skill_finish as mod

    mod.GENERATED_ROOT = tmp_path
    (tmp_path / "run" / "B1").mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (tmp_path / "run" / "B1" / "output.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")
    rc = main(["--run-id", "run", "--skill", "B1", "--no-md"])
    assert rc == 0


def test_finish_skill_success(tmp_path):
    run_dir = tmp_path / "ok"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "output.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")
    assert finish_skill("ok", "B1", generated_root=tmp_path) == 0

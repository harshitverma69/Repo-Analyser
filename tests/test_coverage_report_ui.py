"""Full coverage for runtime.report_ui."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from runtime.report_ui import (
    Theme,
    _box_top,
    _strip_ansi,
    _truncate,
    compute_outcome,
    load_skill_meta,
    render_a5_issues,
    render_b1_highlights,
    render_details,
    render_header,
    render_outcome_panel,
    render_terminal_ui,
)

ROOT = Path(__file__).resolve().parent.parent


def test_theme_no_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    theme = Theme()
    assert theme.wrap("1", "x") == "x"
    assert theme.bold("x") == "x"


def test_theme_colors_when_tty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    theme = Theme()
    assert "\033[" in theme.bold("x")


def test_load_skill_meta_missing_registry(tmp_path, monkeypatch):
    monkeypatch.setattr("runtime.report_ui.REGISTRY_PATH", tmp_path / "missing.json")
    assert load_skill_meta("B1") == {}


def test_truncate_and_strip_ansi():
    assert _truncate("hello", 10) == "hello"
    assert _truncate("hello world", 8) == "hello w…"
    assert _strip_ansi("\033[1mhi\033[0m") == "hi"


def test_box_top_with_title():
    assert "─" in _box_top("Outcome")


def test_compute_outcome_a5_blocking():
    payload = {
        "issues": [{"severity": "blocking", "id": "I1"}],
        "review_target": {"repository_path": "/repo", "diff_or_pr_ref": "HEAD"},
        "generated_at": "t",
    }
    label, tone, headline, metrics = compute_outcome("A5", payload)
    assert label == "NEEDS FIX"
    assert tone == "warn"


def test_compute_outcome_a5_reviewed_and_clean():
    reviewed, _, _, _ = compute_outcome("A5", {"issues": [{"severity": "info"}]})
    assert reviewed == "REVIEWED"
    clean, tone, _, _ = compute_outcome("A5", {"issues": []})
    assert clean == "CLEAN"
    assert tone == "ok"


def test_compute_outcome_b1_empty():
    label, tone, _, _ = compute_outcome("B1", {"files_scanned": 0, "artifacts": {}})
    assert label == "EMPTY"
    assert tone == "warn"


def test_compute_outcome_b2_no_routes():
    label, _, _, _ = compute_outcome("B2", {"endpoints": []})
    assert label == "NO ROUTES"


def test_compute_outcome_b3_tests_fail_and_discovered():
    fail, tone, _, _ = compute_outcome("B3", {"framework": "pytest", "command_result": {"exit_code": 1}})
    assert fail == "TESTS FAIL"
    assert tone == "fail"
    discovered, _, _, _ = compute_outcome("B3", {"framework": "pytest", "test_files": ["t.py"]})
    assert discovered == "DISCOVERED"


def test_compute_outcome_i1_no_schema():
    label, _, _, _ = compute_outcome("I1", {"tables": []})
    assert label == "NO SCHEMA"


def test_compute_outcome_i2_incomplete():
    label, _, _, _ = compute_outcome("I2", {"steps": []})
    assert label == "INCOMPLETE"


def test_compute_outcome_i6_fixed_and_diagnosed():
    fixed, _, _, _ = compute_outcome(
        "I6",
        {"root_cause": {"file_path": "a.py"}, "fix_verified": True},
    )
    assert fixed == "FIXED"
    diagnosed, _, _, _ = compute_outcome("I6", {"root_cause": {"file_path": "a.py"}})
    assert diagnosed == "DIAGNOSED"


def test_compute_outcome_generic_incomplete_and_warnings():
    incomplete, tone, _, _ = compute_outcome("D1", {"scan_complete": False})
    assert incomplete == "INCOMPLETE"
    assert tone == "warn"
    complete, tone, _, _ = compute_outcome("D1", {"warnings": ["w"], "scan_complete": True})
    assert complete == "COMPLETE"
    assert tone == "warn"
    ok, tone, _, _ = compute_outcome("D1", {"scan_complete": True})
    assert ok == "COMPLETE"
    assert tone == "ok"


def test_render_a5_issues_rich():
    theme = Theme()
    issues = [
        {
            "id": "X1",
            "severity": "blocking",
            "category": "security",
            "file_path": "a.py",
            "line": 10,
            "description": "x" * 100,
            "suggested_fix": "fix it",
            "verification_steps": ["step1", "step2"],
        }
    ]
    lines = render_a5_issues(issues, theme)
    text = "\n".join(lines)
    assert "X1" in text
    assert "fix" in text


def test_render_a5_issues_empty():
    theme = Theme()
    assert "No issues" in render_a5_issues([], theme)[0]


def test_render_b1_highlights_many_and_empty():
    theme = Theme()
    items = [{"name": f"n{i}", "file_path": f"p{i}.py"} for i in range(10)]
    lines = render_b1_highlights({"artifacts": {"services": items}}, theme)
    assert "more" in "\n".join(lines)
    assert "No artifacts" in render_b1_highlights({}, theme)[0]


def test_render_details_branches():
    theme = Theme()
    b2 = render_details("B2", {"endpoints": [{"method": "GET", "route": "/h", "handler": "h"}] * 20}, theme)
    assert "more" in "\n".join(b2)
    b3 = render_details(
        "B3",
        {"framework": "pytest", "config_file": "pyproject.toml", "commands": [{"command": "pytest"}]},
        theme,
    )
    assert "pytest" in "\n".join(b3)
    generic = render_details("D1", {"scan_complete": True, "resource_count": 3, "limitations": ["lim"]}, theme)
    assert "Limitations" in "\n".join(generic)


def test_render_header_and_terminal_ui():
    golden = json.loads(
        (ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json").read_text(encoding="utf-8")
    )
    theme = Theme()
    meta = {"name": "Inventory", "level": "BASIC", "level_code": "B", "description": "desc"}
    header = render_header("run-1", "B1", meta, theme)
    assert "B1" in "\n".join(header)
    panel = render_outcome_panel("OK", "ok", "headline", [("K", "V")], theme)
    assert "headline" in "\n".join(panel)
    ui = render_terminal_ui("run-1", "B1", golden)
    assert "B1" in ui

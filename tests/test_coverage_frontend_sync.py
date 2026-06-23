"""Full coverage for runtime.frontend_sync."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from runtime.frontend_sync import (
    _ensure_frontend_data,
    _frontend_port,
    _load_index,
    _load_live,
    ensure_frontend_server,
    frontend_is_running,
    open_skill_report,
    publish_skill_run,
    sync_from_skill_dir,
)

ROOT = Path(__file__).resolve().parent.parent


def test_frontend_port_invalid(monkeypatch):
    monkeypatch.setenv("REPO_ANALYSER_FRONTEND_PORT", "not-a-port")
    assert _frontend_port() == 8765


def test_frontend_is_running_false(monkeypatch):
    import runtime.frontend_sync as mod

    def boom(*_a, **_k):
        raise OSError("nope")

    monkeypatch.setattr(mod.socket, "create_connection", boom)
    assert frontend_is_running(9999) is False


def test_ensure_frontend_data_missing_script(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "FRONTEND_DATA", tmp_path / "data")
    assert _ensure_frontend_data() is False


def test_ensure_frontend_data_subprocess_fail(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "FRONTEND_DATA", tmp_path / "data")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "build_frontend.py").write_text("# stub", encoding="utf-8")

    def fail(*_a, **_k):
        raise subprocess.CalledProcessError(1, "cmd")

    monkeypatch.setattr(mod.subprocess, "run", fail)
    assert _ensure_frontend_data() is False


def test_ensure_frontend_data_success(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    data = tmp_path / "data"
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "FRONTEND_DATA", data)
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "build_frontend.py").write_text("# stub", encoding="utf-8")

    def ok(*_a, **_k):
        data.mkdir(parents=True)
        (data / "skills.json").write_text("{}", encoding="utf-8")
        return subprocess.CompletedProcess([], 0)

    monkeypatch.setattr(mod.subprocess, "run", ok)
    assert _ensure_frontend_data() is True


def test_ensure_frontend_server_paths(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    monkeypatch.setenv("REPO_ANALYSER_AUTO_FRONTEND", "1")
    monkeypatch.setenv("REPO_ANALYSER_AUTO_START_FRONTEND", "1")
    monkeypatch.setattr(mod, "FRONTEND_DIR", tmp_path / "frontend")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "frontend_is_running", lambda port=None: False)

    assert ensure_frontend_server() is False

    frontend = tmp_path / "frontend"
    frontend.mkdir()
    (frontend / "index.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(mod, "_ensure_frontend_data", lambda: False)
    assert ensure_frontend_server() is False

    monkeypatch.setattr(mod, "_ensure_frontend_data", lambda: True)
    assert ensure_frontend_server() is False

    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "serve_frontend.py").write_text("# stub", encoding="utf-8")

    def popen_fail(*_a, **_k):
        raise OSError("fail")

    monkeypatch.setattr(mod.subprocess, "Popen", popen_fail)
    assert ensure_frontend_server() is False

    calls = {"n": 0}

    def running_after_delay(port=None):
        calls["n"] += 1
        return calls["n"] > 2

    monkeypatch.setattr(mod.subprocess, "Popen", lambda *_a, **_k: object())
    monkeypatch.setattr(mod, "frontend_is_running", running_after_delay)
    assert ensure_frontend_server() is True


def test_ensure_frontend_server_timeout(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    frontend = tmp_path / "frontend"
    frontend.mkdir()
    (frontend / "index.html").write_text("<html></html>", encoding="utf-8")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "serve_frontend.py").write_text("# stub", encoding="utf-8")

    monkeypatch.setenv("REPO_ANALYSER_AUTO_FRONTEND", "1")
    monkeypatch.setenv("REPO_ANALYSER_AUTO_START_FRONTEND", "1")
    monkeypatch.setattr(mod, "FRONTEND_DIR", frontend)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "_ensure_frontend_data", lambda: True)
    monkeypatch.setattr(mod, "frontend_is_running", lambda port=None: False)
    monkeypatch.setattr(mod.subprocess, "Popen", lambda *_a, **_k: object())
    tick = {"v": 0.0}

    def fake_monotonic():
        tick["v"] += 0.2
        return tick["v"]

    monkeypatch.setattr(mod.time, "monotonic", fake_monotonic)
    assert ensure_frontend_server() is False


def test_open_skill_report_disabled_and_markdown_fallback(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    assert open_skill_report("r", "B1", open_browser=False) is None

    md = tmp_path / "out.md"
    md.write_text("# hi", encoding="utf-8")
    opened: list[str] = []
    monkeypatch.setattr(mod.webbrowser, "open", lambda url: opened.append(url) or True)
    monkeypatch.setattr(mod, "ensure_frontend_server", lambda port=None: False)
    monkeypatch.setattr(mod, "frontend_is_running", lambda port=None: False)
    uri = open_skill_report("r", "B1", markdown_path=md, open_browser=True)
    assert uri is not None
    assert opened


def test_publish_opens_browser(capsys, tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    monkeypatch.setattr(mod, "FRONTEND_DATA", tmp_path)
    monkeypatch.setenv("REPO_ANALYSER_AUTO_FRONTEND", "1")
    monkeypatch.setattr(mod, "ensure_frontend_server", lambda port=None: True)
    monkeypatch.setattr(mod, "frontend_is_running", lambda port=None: True)
    monkeypatch.setattr(mod.webbrowser, "open", lambda url: True)

    payload = {"task_id": "B1", "level": "B", "scan_complete": True, "artifacts": {}, "files_scanned": 1}
    publish_skill_run("run", "B1", payload)
    assert "Opened report" in capsys.readouterr().out


def test_load_index_and_live(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    monkeypatch.setattr(mod, "FRONTEND_DATA", tmp_path)
    assert _load_index() == {"runs": {}}
    assert _load_live() == {"latest": None, "history": []}
    (tmp_path / "runs_index.json").write_text('{"runs": {"a": {}}}', encoding="utf-8")
    (tmp_path / "live.json").write_text('{"latest": null, "history": []}', encoding="utf-8")
    assert "a" in _load_index()["runs"]


def test_sync_from_skill_dir(tmp_path, monkeypatch):
    import runtime.frontend_sync as mod

    monkeypatch.setattr(mod, "FRONTEND_DATA", tmp_path)
    monkeypatch.setenv("REPO_ANALYSER_AUTO_FRONTEND", "0")
    run_dir = tmp_path / "runs-root"
    skill_dir = run_dir / "B1"
    skill_dir.mkdir(parents=True)
    golden = ROOT / "generated_projects" / "_golden" / "B1" / "inventory_report.json"
    (skill_dir / "inventory_report.json").write_text(golden.read_text(encoding="utf-8"), encoding="utf-8")
    result = sync_from_skill_dir(run_dir, "B1")
    assert result is not None
    assert sync_from_skill_dir(tmp_path / "empty", "B1") is None

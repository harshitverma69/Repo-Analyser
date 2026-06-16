"""Tests for repolens eval runner helpers."""

from __future__ import annotations

from pathlib import Path

from tools.repolens_eval_runner import DEFAULT_REPO, ROOT, _envelope


def test_default_repo_is_sibling_of_repo_analyser():
    assert DEFAULT_REPO == ROOT.parent / "repolens"


def test_envelope_uses_passed_repo(tmp_path: Path):
    repo = tmp_path / "custom-target"
    repo.mkdir()
    payload = _envelope("B1", "B", repo)
    assert payload["repository_path"] == str(repo)
    assert payload["task_id"] == "B1"

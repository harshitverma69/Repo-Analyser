"""Tests for expand_agent_specs generator."""

from __future__ import annotations

from pathlib import Path

from tools.expand_agent_specs import _golden_schema, render_agent

ROOT = Path(__file__).resolve().parent.parent


def test_golden_schema_b1():
    schema = _golden_schema("B1")
    assert '"task_id": "B1"' in schema
    assert '"artifacts"' in schema


def test_render_agent_single_json_block():
    content = render_agent("B1")
    assert content.count("```json") == 1
    assert "### Outputs (STRICT JSON)" in content
    assert "## Output contract (STRICT JSON)" not in content


def test_render_agent_has_phases():
    content = render_agent("A5")
    assert "Phase 2 — Adversarial review" in content
    assert "skill_finish write" in content


def test_main_expands_all_agents():
    from tools import expand_agent_specs

    assert expand_agent_specs.main() == 0
    path = ROOT / "agents" / "basics" / "B1_repo_artifact_inventory_agent.md"
    assert path.is_file()
    assert path.read_text(encoding="utf-8").count("```json") == 1

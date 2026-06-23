"""Tests for plugin discovery and registry."""

from __future__ import annotations

from runtime.models import RunContext, SkillResult
from runtime.plugins import PluginRegistry, discover_plugins
from runtime.plugins.base import BaseSkillPlugin


class StubPlugin(BaseSkillPlugin):
    id = "STUB"
    version = "0.1.0"

    def execute(self, context: RunContext) -> SkillResult:
        return SkillResult(
            skill_id=self.id,
            status="complete",
            output_path="",
            started_at="t",
            completed_at="t",
        )


def test_plugin_registry_register_and_get():
    registry = PluginRegistry()
    plugin = StubPlugin()
    registry.register(plugin)
    assert registry.get("STUB") is plugin
    assert registry.get("stub") is plugin


def test_discover_plugins_loads_all_skills():
    registry = discover_plugins()
    ids = registry.skill_ids()
    assert "B1" in ids
    assert len(ids) >= 24

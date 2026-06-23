"""In-memory plugin registry."""

from __future__ import annotations

from runtime.plugins.base import SkillPlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, SkillPlugin] = {}

    def register(self, plugin: SkillPlugin) -> None:
        self._plugins[plugin.id.upper()] = plugin

    def get(self, skill_id: str) -> SkillPlugin | None:
        return self._plugins.get(skill_id.upper())

    def all_plugins(self) -> list[SkillPlugin]:
        return sorted(self._plugins.values(), key=lambda plugin: plugin.id)

    def skill_ids(self) -> list[str]:
        return sorted(self._plugins.keys())

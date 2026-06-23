# Plugin API

Skills implement the `SkillPlugin` protocol:

```python
from runtime.plugins.base import SkillPlugin
from runtime.models import RunContext, SkillResult

class MyPlugin:
    id = "B1"
    version = "1.0.0"

    def execute(self, context: RunContext) -> SkillResult:
        ...
```

## Discovery

```python
from runtime.plugins import discover_plugins

registry = discover_plugins()
plugin = registry.get("B1")
result = plugin.execute(context)
```

Plugins are auto-registered from `core/skill_registry.json` + `skills/**/*.skill.md`.
The default implementation is `GoldenReplayPlugin` (deterministic golden copy).

## Registry

```python
from runtime.plugins.registry import PluginRegistry

registry = PluginRegistry()
registry.register(my_plugin)
assert registry.get("B1") is my_plugin
```

## Extending

1. Subclass `BaseSkillPlugin` or satisfy `SkillPlugin` protocol
2. Register manually or add to a discoverable builtins module
3. Keep `execute()` pure/deterministic for CI compatibility

See [extension_guide.md](extension_guide.md).

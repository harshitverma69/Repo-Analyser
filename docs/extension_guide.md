# Extension Guide

## Add a new skill

1. Add agent spec under `agents/{level}/`
2. Add eval blueprint under `eval_blueprints/{level}/`
3. Add golden JSON under `generated_projects/_golden/{ID}/`
4. Run `make build-skills` to regenerate `.skill.md` + registry
5. Run `make validate-dag`

## Add a custom plugin

```python
# runtime/plugins/builtins/my_plugin.py
from runtime.plugins.base import BaseSkillPlugin
from runtime.models import RunContext, SkillResult

class CustomB1Plugin(BaseSkillPlugin):
    id = "B1"
    version = "2.0.0"

    def execute(self, context: RunContext) -> SkillResult:
        ...
```

Register in tests or extend `loader.py` discovery as needed.

## Expand agent specs

```bash
make expand-agent-specs
# tools/expand/cli.py → updates agents/*_agent.md
```

## Run locally with coverage

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
make test
make harden
```

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

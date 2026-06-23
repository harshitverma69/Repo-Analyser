# Architecture

Repo-Analyser is a deterministic eval framework for repository analysis tasks (PML/OCL 24-skill pipeline).

## Layers

```
skills/              Markdown skill specs (.skill.md)
core/                Registry, execution rules, eval source
runtime/
  models.py          Typed dataclasses (SkillSpec, RunContext, …)
  orchestrator/      DAG planning, execution, aggregation
  plugins/           SkillPlugin protocol + golden-replay plugins
  reporting/         JSON/Markdown report writers
  skill_runner.py    Public runner API (backward compatible)
  skill_orchestrator.py  Public orchestrator API
tools/
  expand/            Agent spec expansion (parser, compiler, CLI)
generated_projects/  Run outputs + _golden reference JSON
```

## Design principles

- **Deterministic CI path:** `SkillRunner` replays golden JSON; no LLM in automated runs.
- **Live eval path:** Cursor agents write real outputs via `skill_finish write`.
- **Stable public API:** `runtime.skill_runner` and `runtime.skill_orchestrator` remain import paths.
- **Composition:** Orchestrator delegates to planner, dependency_resolver, executor, result_aggregator.

## Module boundaries

| Package | Responsibility |
|---------|----------------|
| `orchestrator/planner.py` | Discover skills, build plans, validate DAG |
| `orchestrator/dependency_resolver.py` | Topological sort, cycles, orphans |
| `orchestrator/executor.py` | Golden replay execution engine |
| `orchestrator/result_aggregator.py` | execution_log.json + final_report.json |
| `plugins/` | Auto-discovered SkillPlugin implementations |

See also: [execution_flow.md](execution_flow.md), [plugin_api.md](plugin_api.md).

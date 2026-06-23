# Migration Summary

Production-hardening refactor (2026-06-17).

## Completed

1. **RepoLens removed** — eval runner, tests, docs, generated artifacts, Makefile target
2. **Orchestrator package** — `runtime/orchestrator/{planner,executor,dependency_resolver,result_aggregator,cli}.py`
3. **Typed models** — `runtime/models.py` (SkillSpec, SkillDependency, SkillResult, RunContext, ExecutionReport)
4. **Plugin architecture** — `runtime/plugins/{base,loader,registry}.py`
5. **Reporting package** — `runtime/reporting/` (renderer re-exports + json_writer)
6. **Expand split** — `tools/expand/{parser,validator,compiler,template_engine,cli}.py` + `phases_data.py`
7. **Tooling** — ruff, black, mypy, pre-commit, pytest-cov in `pyproject.toml`
8. **CI** — `.github/workflows/ci.yml` (lint, typecheck, tests, DAG, golden determinism)
9. **Documentation** — `docs/architecture.md`, `execution_flow.md`, `plugin_api.md`, etc.

## Backward compatibility

| Import / CLI | Status |
|--------------|--------|
| `from runtime.skill_runner import SkillRunner` | ✅ unchanged |
| `from runtime.skill_orchestrator import SkillOrchestrator` | ✅ unchanged |
| `python -m runtime.skill_orchestrator --validate-dag` | ✅ unchanged |
| `tools.expand_agent_specs` | ✅ re-exports from `tools.expand` |
| `make harden`, `make test-determinism` | ✅ unchanged |

## Behavior

Deterministic golden replay outputs remain byte-identical. No breaking API changes.

## Follow-up (optional)

- Further split `report_renderer.py` (~466 LOC) into reporting submodules — **done** (`formatters`, `handlers`, `loader`, `meta`, `renderer`, `markdown_writer`)
- Split `skill_registry_builder.py` if it grows
- Add JSON Schema files per task

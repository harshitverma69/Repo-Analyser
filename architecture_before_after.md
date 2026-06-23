# Architecture Before / After

## Before

```
runtime/
  skill_orchestrator.py   (~318 LOC, monolithic)
  skill_runner.py         (~318 LOC, monolithic)
  report_renderer.py      (~466 LOC)
tools/
  expand_agent_specs.py   (~1148 LOC)
tools/
  repolens_eval_runner.py (removed)
```

- Dict-heavy internal APIs
- No plugin layer
- No CI workflows
- RepoLens bridge (unused)

## After

```
runtime/
  models.py
  skill_orchestrator.py   (thin facade)
  skill_runner.py         (thin facade)
  orchestrator/
    planner.py
    executor.py
    dependency_resolver.py
    result_aggregator.py
    cli.py
  plugins/
    base.py, loader.py, registry.py
  reporting/
    models.py, json_writer.py, markdown_writer.py, renderer.py
tools/
  expand_agent_specs.py   (thin facade)
  expand/
    parser.py, validator.py, compiler.py, template_engine.py, cli.py, phases_data.py
.github/workflows/ci.yml
docs/architecture.md, ...
```

## Quality improvements

| Area | Before | After |
|------|--------|-------|
| Largest runtime module | ~318 LOC | ~190 LOC (compiler) |
| Typed models | Partial | SkillSpec, RunContext, ExecutionReport, … |
| Plugin extensibility | None | SkillPlugin + auto-discovery |
| CI | Manual `make harden` only | GitHub Actions + local lint/typecheck |
| Dead code | RepoLens bridge | Removed |

Public entry points unchanged.

# Design Decisions

## Backward-compatible module paths

`runtime/skill_runner.py` and `runtime/skill_orchestrator.py` remain thin facades so existing imports and CLI entry points (`python -m runtime.skill_orchestrator`) work unchanged.

## Golden replay vs live analysis

CI and `make harden` use golden JSON replay for reproducibility. Live Cursor runs perform real analysis and write via `skill_finish`.

## Dataclasses over raw dicts

`SkillSpec`, `SkillResult`, `RunContext`, and `ExecutionReport` replace ad-hoc dict assembly in orchestrator/executor paths. Legacy `.to_dict()` preserves JSON shape.

## Plugin layer

Plugins wrap the executor without changing runner behavior. Default plugins map 1:1 to registry skills.

## RepoLens removal

RepoLens bridge (`repolens_eval_runner`, bridge docs) was removed as unused. Repo-Analyser is standalone; eval lineage is documented in `core/eval_source.md`.

## Module size limits

Files >300 LOC split into packages:
- `runtime/orchestrator/`
- `runtime/reporting/`
- `tools/expand/`

`phases_data.py` holds large static phase tables (data, not logic).

## Tooling

Ruff, Black, mypy, pre-commit, pytest-cov, and GitHub Actions enforce quality without changing runtime behavior.

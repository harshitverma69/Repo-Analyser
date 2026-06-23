# Deleted Files

RepoLens and bridge artifacts removed in production-hardening refactor:

| Path | Reason |
|------|--------|
| `tools/repolens_eval_runner.py` | Unused RepoLens eval bridge |
| `tests/test_repolens_eval_runner.py` | Tests for removed bridge |
| `docs/repolens_bridge.md` | Obsolete documentation |
| `generated_projects/repolens/` | Generated eval artifacts |
| `frontend/data/runs/repolens/` | Frontend run data for RepoLens |

## Makefile targets removed

- `repolens-eval`

## References cleaned

- `docs/OVERVIEW.md` — Integration with RepoLens section removed
- `docs/STATUS.md` — RepoLens bridge doc row removed
- `Makefile` help text updated

Note: `tests/test_frontend_sync.py` uses `"repolens"` as a generic example `run_id` only (not a dependency on RepoLens).

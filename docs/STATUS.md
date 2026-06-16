# CAC-OS Project Status

Last updated: 2026-06-16

## Summary

CAC-OS is a **spec-complete** deterministic framework for the PML/OCL 24-task coding agent eval. All agent specs, blueprints, validation rules, golden examples, and tooling are in place. **Live eval execution** (actually building services, running Terraform, etc.) is done by engineers/Cursor per run — outputs go in `generated_projects/{run_id}/`.

---

## Done ✅

### Phase 1 — Eval alignment (complete)

| Item | Status | Location |
|------|--------|----------|
| Map PML/OCL eval (24 tasks) | ✅ | `core/eval_source.md` |
| Agent specs (24) | ✅ | `agents/**/*_agent.md` |
| Eval blueprints (24) | ✅ | `eval_blueprints/{B,I,A,D}/` |
| Capability registry | ✅ | `core/capability_registry.md` |
| Execution rules | ✅ | `core/execution_rules.md` |
| Validation matrix | ✅ | `core/validation_matrix.md` |
| Task router + DAG | ✅ | `execution_models/` |
| Output contracts | ✅ | `verification/output_contracts.md` |
| Deterministic checks | ✅ | `verification/deterministic_checks.md` |
| Self-eval checklist | ✅ | `core/self_eval_checklist.md` |

### Phase 2 — Tooling & reference outputs (complete)

| Item | Status | Location |
|------|--------|----------|
| Machine-readable task registry | ✅ | `scripts/task_registry.json` |
| Skill registry (compiled) | ✅ | `core/skill_registry.json` |
| Skill execution runtime | ✅ | `runtime/` |
| Deterministic runner/validator | ✅ | `runtime/skill_runner.py`, `scripts/cac_os.py` |
| Cursor skill installer | ✅ | `tools/install_cursor_skills.py` |
| How-to-run guide (all 24 skills) | ✅ | `docs/HOW_TO_RUN.md` |
| Makefile shortcuts | ✅ | `Makefile` |
| Golden JSON examples (24 tasks) | ✅ | `generated_projects/_golden/` |
| Golden manifest | ✅ | `generated_projects/_golden/manifest.json` |
| Registry validation (automated) | ✅ | `make validate` passes |
| RepoLens bridge doc | ✅ | `docs/repolens_bridge.md` |
| Project README | ✅ | `README.md` |
| Architecture overview | ✅ | `docs/OVERVIEW.md` |

### Phase 3 — Naming & structure (complete)

| Item | Status | Notes |
|------|--------|-------|
| Renamed `agents_md/` → `agents/` | ✅ | |
| `*_agent.md` file naming | ✅ | e.g. `B4_fastapi_greenfield_agent.md` |
| Removed old RepoLens-only tasks (B7-B8, I7, etc.) | ✅ | Documented in `eval_source.md` |

---

## Not Done (by design — live eval work)

These are **intentionally outside** the CAC-OS spec repo. Each engineer/Cursor run produces them in `generated_projects/{run_id}/`:

| Item | Description | How to complete |
|------|-------------|-----------------|
| Live B4 FastAPI service | Real code + passing tests | Run eval per `B4_*_agent.md` |
| Live B5/B6 greenfield | Node + Rust projects | Run B5, B6 specs |
| Live I4 polyglot pair | FastAPI + Node client | Run I4 spec |
| Live A3 fraud system | 3-component system | Run A3 spec |
| Live D1 Terraform | `terraform validate/plan` proof | Run D1 spec |
| Live D2 compose E2E | Full stack + e2e script | Run D2 spec |
| Live D3 CI green run | GitHub Actions / act | Run D3 spec |
| Live D4 K8s deploy | kind/minikube + curl | Run D4 spec |
| Live D5 bootstrap | Fresh clone single command | Run D5 spec |
| Live D6 observability | Prometheus + Grafana panel | Run D6 spec |
| Per-engineer self-eval marks | yes/no in checklist | `core/self_eval_checklist.md` |

---

## Validation Status

```bash
$ make validate
OK: 24 tasks, all specs/blueprints/golden examples present, DAG acyclic
```

---

## Coverage Matrix

| Level | Tasks | Specs | Blueprints | Golden JSON | Validator |
|-------|-------|-------|------------|-------------|-----------|
| B | 6 | 6/6 | 6/6 | 6/6 | ✅ |
| I | 6 | 6/6 | 6/6 | 6/6 | ✅ |
| A | 6 | 6/6 | 6/6 | 6/6 | ✅ |
| D | 6 | 6/6 | 6/6 | 6/6 | ✅ |
| **Total** | **24** | **100%** | **100%** | **100%** | **✅** |

---

## Optional Future Enhancements

| Enhancement | Priority | Notes |
|-------------|----------|-------|
| JSON Schema files (`.schema.json`) per task | Low | Currently documented in MD + golden |
| GitHub Action to run `make validate` on PR | Medium | CI for the spec repo itself |
| RepoLens → CAC-OS transform script | Medium | Auto-convert ApiMapReport → B2 JSON |
| Example live run folder | Low | `generated_projects/example-live-run/` after someone completes B4 |

---

## History

| Date | Milestone |
|------|-----------|
| 2026-06-16 | Initial CAC-OS from RepoLens capability-matrix (27 tasks) |
| 2026-06-16 | Realigned to PML/OCL eval (24 tasks); renamed to `agents/*_agent.md` |
| 2026-06-16 | Added golden examples, `cac_os.py`, docs, Makefile, self-eval checklist |

---

## Next Step for You

1. Read **[docs/HOW_TO_RUN.md](HOW_TO_RUN.md)** — setup, commands, and every skill with role + locations
2. Run: `make build-skills && make install-cursor-skills && make validate`
3. Pick one task (start with **B1** or **B3** on a repo you know)
4. Type `/cac-os-repo-inventory` in Cursor, or `make run-skill SKILL=B1 RUN_ID=my-run`
5. Validate: `make validate-run RUN_DIR=generated_projects/my-run`

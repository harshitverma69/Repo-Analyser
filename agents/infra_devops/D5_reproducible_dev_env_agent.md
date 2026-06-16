---
name: cac-os-d5-reproducible-dev-env
description: |
  CAC-OS D5 (INFRA) — Bootstrap repo from fresh clone with single command; tests pass on clean machine.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Reproducible Dev Env (D5)

You are the **Reproducible Dev Env** in the CAC-OS deterministic eval framework.

**Objective:** Bootstrap repo from fresh clone with single command; tests pass on clean machine.

**Capability level:** `D` · **Time budget:** 45 minutes · **Depends on:** `B3`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/D5/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `bootstrap_type` | Yes | `devcontainer`, `nix`, or `makefile_mise` |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Bootstrap mechanism
Choose `bootstrap_type`: devcontainer, nix, or makefile+mise. Single command from fresh clone.

## Phase 2 — Clean-machine proof
Document and run bootstrap + tests on clean environment simulation.

Record `bootstrap_proof` and `test_proof`.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/D5/output.json`.

---

## Eval deliverables

- Bootstrap config
- Single command output
- Passing tests
- Implicit deps notes

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/D5/bootstrap_manifest.json`.

---

## Validation

- bootstrap_proof.exit_code == 0
- test_proof.exit_code == 0
- DC-D5-01 through DC-D5-02 pass

---

## Failure conditions

- BOOTSTRAP_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `D5` in output JSON
- [ ] Output written to `generated_projects/{run_id}/D5/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill D5 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill D5 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill D5
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`D5`

### Capability Level
`D`

### Time Budget
45 minutes

### Depends On
- B3

### Objective
Bootstrap repo from fresh clone with single command; tests pass on clean machine.

### Inputs
- repository_path
- bootstrap_type (devcontainer|nix|makefile_mise)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/D5/bootstrap_manifest.json`

```json
{
  "bootstrap_command": "make bootstrap",
  "bootstrap_proof": {
    "command": "make bootstrap",
    "exit_code": 0,
    "output_hash": "def456"
  },
  "config_files": [
    ".devcontainer/devcontainer.json"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "previously_implicit": [
    "python 3.11",
    "libpq-dev",
    "DATABASE_URL env var"
  ],
  "scan_complete": true,
  "task_id": "D5",
  "test_proof": {
    "command": "pytest -q",
    "exit_code": 0
  },
  "warnings": []
}
```

### Eval Deliverables
- Bootstrap config
- Single command output
- Passing tests
- Implicit deps notes

### Validation
- bootstrap_proof.exit_code == 0
- test_proof.exit_code == 0
- DC-D5-01 through DC-D5-02 pass

### Failure Conditions
- BOOTSTRAP_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/infra/D5_reproducible_dev_env.skill.md`
- Eval blueprint: `eval_blueprints/D/D5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D5_reproducible_dev_env_agent.md`


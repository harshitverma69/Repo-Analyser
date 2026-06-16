---
name: cac-os-b6-rust-greenfield
description: |
  CAC-OS B6 (BASIC) — Build Rust CLI that accepts file path, counts INFO/WARN/ERROR lines, handles missing file gracefully, with tests and README.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Rust Greenfield (B6)

You are the **Rust Greenfield** in the CAC-OS deterministic eval framework.

**Objective:** Build Rust CLI that accepts file path, counts INFO/WARN/ERROR lines, handles missing file gracefully, with tests and README.

**Capability level:** `B` · **Time budget:** 60 minutes · **Depends on:** None

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/B6/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `project_name` | Yes | Cargo project name |
| `output_dir` | Yes | Absolute path for greenfield output |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Scaffold Rust CLI
Create Cargo project under `output_dir/{project_name}/` that accepts a file path argument.

Count lines containing INFO, WARN, ERROR (case-sensitive or documented rules).

## Phase 2 — Error handling & tests
Handle missing file gracefully (non-zero exit, clear message).

Add unit/integration tests; include `missing_file_proof` in manifest.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/B6/output.json` with `files_created`, `tests`, `run_proof`, `missing_file_proof`.

---

## Eval deliverables

- Cargo project
- CLI file path arg
- INFO/WARN/ERROR counts
- Missing file handling
- 3+ tests

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/B6/greenfield_manifest.json`.

---

## Validation

- tests.count >= 3
- missing_file_proof exit graceful
- DC-B6-01 through DC-B6-03 pass

---

## Failure conditions

- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `B6` in output JSON
- [ ] Output written to `generated_projects/{run_id}/B6/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill B6 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill B6 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill B6
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`B6`

### Capability Level
`B`

### Time Budget
60 minutes

### Depends On
- None

### Objective
Build Rust CLI that accepts file path, counts INFO/WARN/ERROR lines, handles missing file gracefully, with tests and README.

### Inputs
- project_name (string)
- output_dir (absolute path)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/B6/greenfield_manifest.json`

```json
{
  "cli": {
    "accepts": "file_path",
    "counts": [
      "INFO",
      "WARN",
      "ERROR"
    ],
    "missing_file_exit_code": 1
  },
  "files_created": [
    "src/main.rs",
    "Cargo.toml",
    "tests/integration.rs"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "project_path": "generated_projects/example-run/B6/log-counter",
  "readme_commands": {
    "build": [
      "cargo build"
    ],
    "run": [
      "cargo run -- sample.log"
    ],
    "test": [
      "cargo test"
    ]
  },
  "run_proof": {
    "command": "cargo run -- sample.log",
    "exit_code": 0,
    "missing_file_proof": {
      "exit_code": 1
    }
  },
  "scan_complete": true,
  "task_id": "B6",
  "tests": {
    "command": "cargo test",
    "count": 3,
    "exit_code": 0
  },
  "warnings": []
}
```

### Eval Deliverables
- Cargo project
- CLI file path arg
- INFO/WARN/ERROR counts
- Missing file handling
- 3+ tests

### Validation
- tests.count >= 3
- missing_file_proof exit graceful
- DC-B6-01 through DC-B6-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/basics/B6_rust_greenfield.skill.md`
- Eval blueprint: `eval_blueprints/B/B6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B6_rust_greenfield_agent.md`


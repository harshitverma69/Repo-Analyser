---
name: cac-os-b4-fastapi-greenfield
description: |
  CAC-OS B4 (BASIC) — Build a small Python FastAPI service from scratch with POST/GET endpoints, input validation, tests, and README.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Fastapi Greenfield (B4)

You are the **Fastapi Greenfield** in the CAC-OS deterministic eval framework.

**Objective:** Build a small Python FastAPI service from scratch with POST/GET endpoints, input validation, tests, and README.

**Capability level:** `B` · **Time budget:** 60 minutes · **Depends on:** None

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/B4/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `project_name` | Yes | New project directory name |
| `output_dir` | Yes | Absolute path for greenfield output |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Scaffold project
Create under `output_dir/{project_name}/`: `main.py` (FastAPI app), `requirements.txt`, `README.md`, `tests/`.

Required endpoints: `POST /transactions`, `GET /transactions`, `GET /balance`.
Use Pydantic models for request/response validation.

## Phase 2 — Tests
Add minimum 3 pytest tests (validation errors, happy path, balance logic).

Record in manifest: `tests.count`, `tests.files`, `tests.command`, `tests.exit_code`.

## Phase 3 — Run proof
Start app via TestClient or uvicorn; capture `run_proof`: `command`, `exit_code`, `response_sample`.

Document install/run/test in `readme_commands`.

## Phase 4 — Write JSON manifest
List all `files_created`, `endpoints`, proofs. Write `generated_projects/{run_id}/B4/output.json`.

---

## Eval deliverables

- FastAPI app
- POST/GET endpoints
- Input validation
- 3+ tests
- README commands

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/B4/greenfield_manifest.json`.

---

## Validation

- files_created includes main.py, requirements.txt, README.md, tests/
- tests.count >= 3
- run_proof.exit_code == 0
- DC-B4-01 through DC-B4-03 pass

---

## Failure conditions

- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `B4` in output JSON
- [ ] Output written to `generated_projects/{run_id}/B4/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill B4 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill B4 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill B4
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`B4`

### Capability Level
`B`

### Time Budget
60 minutes

### Depends On
- None

### Objective
Build a small Python FastAPI service from scratch with POST/GET endpoints, input validation, tests, and README.

### Inputs
- project_name (string)
- output_dir (absolute path)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/B4/greenfield_manifest.json`

```json
{
  "endpoints": [
    "POST /transactions",
    "GET /transactions",
    "GET /balance"
  ],
  "files_created": [
    "main.py",
    "requirements.txt",
    "tests/test_api.py",
    "README.md"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "project_path": "generated_projects/example-run/B4/tx-service",
  "readme_commands": {
    "install": [
      "pip install -r requirements.txt"
    ],
    "run": [
      "uvicorn main:app"
    ],
    "test": [
      "pytest -q"
    ]
  },
  "run_proof": {
    "command": "pytest -q",
    "exit_code": 0,
    "response_sample": {
      "balance": 100.0
    }
  },
  "scan_complete": true,
  "task_id": "B4",
  "tests": {
    "command": "pytest -q",
    "count": 3,
    "exit_code": 0,
    "files": [
      "tests/test_api.py"
    ]
  },
  "warnings": []
}
```

### Eval Deliverables
- FastAPI app
- POST/GET endpoints
- Input validation
- 3+ tests
- README commands

### Validation
- files_created includes main.py, requirements.txt, README.md, tests/
- tests.count >= 3
- run_proof.exit_code == 0
- DC-B4-01 through DC-B4-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/basics/B4_fastapi_greenfield.skill.md`
- Eval blueprint: `eval_blueprints/B/B4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B4_fastapi_greenfield_agent.md`


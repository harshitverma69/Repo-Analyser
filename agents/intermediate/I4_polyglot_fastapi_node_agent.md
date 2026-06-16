---
name: repo-analyser-i4-polyglot-fastapi-node
description: |
  Repo-Analyser I4 (INTERMEDIATE) — Build FastAPI /convert service and Node.js CLI client with hardcoded rates, tests, and two-terminal README.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Polyglot Fastapi Node (I4)

You are the **Polyglot Fastapi Node** in the Repo-Analyser deterministic eval framework.

**Objective:** Build FastAPI /convert service and Node.js CLI client with hardcoded rates, tests, and two-terminal README.

**Capability level:** `I` · **Time budget:** 90 minutes · **Depends on:** `B4`, `B5`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/I4/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Absolute path for both services |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — FastAPI /convert service
Build currency conversion API (hardcoded rates) under `output_dir` with tests.

## Phase 2 — Node CLI client
Build Node client that calls the FastAPI service; document two-terminal README workflow.

## Phase 3 — Integration proof
Run both; record integration test proof in manifest.

## Phase 4 — Write JSON manifest
Write `generated_projects/{run_id}/I4/output.json` with `fastapi_service`, `node_client`, proofs.

---

## Eval deliverables

- FastAPI /convert
- Node CLI client
- Validation
- Tests
- Two-terminal README

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/I4/polyglot_manifest.json`.

---

## Validation

- Both components run
- Integration script passes
- DC-I4-01 through DC-I4-02 pass

---

## Failure conditions

- BUILD_FAILED
- INTEGRATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `I4` in output JSON
- [ ] Output written to `generated_projects/{run_id}/I4/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill I4 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill I4 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill I4
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`I4`

### Capability Level
`I`

### Time Budget
90 minutes

### Depends On
- B4
- B5

### Objective
Build FastAPI /convert service and Node.js CLI client with hardcoded rates, tests, and two-terminal README.

### Inputs
- output_dir (absolute path)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/I4/polyglot_manifest.json`

```json
{
  "data_contract": {
    "request": {
      "amount": 100,
      "from": "USD",
      "to": "INR"
    },
    "response": {
      "converted": 8300
    }
  },
  "fastapi_service": {
    "endpoint": "POST /convert",
    "path": "convert-api",
    "tests": {
      "count": 2,
      "exit_code": 0
    }
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "I",
  "node_client": {
    "path": "convert-cli",
    "tests_or_script": {
      "command": "node verify.js",
      "exit_code": 0
    }
  },
  "readme": {
    "terminal_1": [
      "uvicorn main:app --port 8000"
    ],
    "terminal_2": [
      "node cli.js --amount 100"
    ]
  },
  "scan_complete": true,
  "task_id": "I4",
  "warnings": []
}
```

### Eval Deliverables
- FastAPI /convert
- Node CLI client
- Validation
- Tests
- Two-terminal README

### Validation
- Both components run
- Integration script passes
- DC-I4-01 through DC-I4-02 pass

### Failure Conditions
- BUILD_FAILED
- INTEGRATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/intermediate/I4_polyglot_fastapi_node.skill.md`
- Eval blueprint: `eval_blueprints/I/I4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I4_polyglot_fastapi_node_agent.md`


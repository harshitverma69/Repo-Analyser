---
name: repo-analyser-a3-polyglot-fraud-system
description: |
  Repo-Analyser A3 (ADVANCED) — Build mini fraud-score system: FastAPI ingestion, Node.js worker, Rust scoring engine with tests and README.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Polyglot Fraud System (A3)

You are the **Polyglot Fraud System** in the Repo-Analyser deterministic eval framework.

**Objective:** Build mini fraud-score system: FastAPI ingestion, Node.js worker, Rust scoring engine with tests and README.

**Capability level:** `A` · **Time budget:** 150 minutes · **Depends on:** `B4`, `B5`, `B6`, `I4`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/A3/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Absolute path for fraud system |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — FastAPI ingestion service
Transaction ingestion API with validation and persistence stub.

## Phase 2 — Node worker + Rust scoring engine
Node.js worker consumes/processes events; Rust engine computes fraud score.

## Phase 3 — Integration tests & README
End-to-end test across three components. Document architecture in README.

## Phase 4 — Write JSON manifest
Write `generated_projects/{run_id}/A3/output.json` with component paths and `tests.integration` proof.

---

## Eval deliverables

- FastAPI ingestion
- Node worker
- Rust scorer
- Data contract
- Tests
- Run order README

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/A3/fraud_system_manifest.json`.

---

## Validation

- All 3 components build
- integration test passes
- DC-A3-01 through DC-A3-02 pass

---

## Failure conditions

- BUILD_FAILED
- INTEGRATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `A3` in output JSON
- [ ] Output written to `generated_projects/{run_id}/A3/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill A3 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill A3 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill A3
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`A3`

### Capability Level
`A`

### Time Budget
150 minutes

### Depends On
- B4
- B5
- B6
- I4

### Objective
Build mini fraud-score system: FastAPI ingestion, Node.js worker, Rust scoring engine with tests and README.

### Inputs
- output_dir (absolute path)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/A3/fraud_system_manifest.json`

```json
{
  "data_contract": {
    "risk_score": {
      "level": "low",
      "score": 0.15
    },
    "transaction": {
      "amount": 100,
      "id": "uuid"
    }
  },
  "fastapi": {
    "endpoint": "POST /transactions",
    "path": "ingestion"
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "A",
  "node_worker": {
    "path": "worker",
    "process": "worker.js"
  },
  "run_order": [
    "cargo build",
    "npm start worker",
    "uvicorn ingestion:app"
  ],
  "rust_engine": {
    "binary": "fraud-score",
    "path": "scorer",
    "type": "cli"
  },
  "scan_complete": true,
  "task_id": "A3",
  "tests": {
    "integration": {
      "exit_code": 0
    },
    "rust_unit": {
      "exit_code": 0
    }
  },
  "warnings": []
}
```

### Eval Deliverables
- FastAPI ingestion
- Node worker
- Rust scorer
- Data contract
- Tests
- Run order README

### Validation
- All 3 components build
- integration test passes
- DC-A3-01 through DC-A3-02 pass

### Failure Conditions
- BUILD_FAILED
- INTEGRATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/advanced/A3_polyglot_fraud_system.skill.md`
- Eval blueprint: `eval_blueprints/A/A3_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A3_polyglot_fraud_system_agent.md`


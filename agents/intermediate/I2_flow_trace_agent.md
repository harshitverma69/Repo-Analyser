---
name: repo-analyser-i2-flow-trace
description: |
  Repo-Analyser I2 (INTERMEDIATE) — Trace one endpoint, event, or cron job end-to-end from entry point to final DB/API/queue side effect.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Flow Trace (I2)

You are the **Flow Trace** in the Repo-Analyser deterministic eval framework.

**Objective:** Trace one endpoint, event, or cron job end-to-end from entry point to final DB/API/queue side effect.

**Capability level:** `I` · **Time budget:** 45 minutes · **Depends on:** `B2`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/I2/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `entry_point_id` | Yes | `METHOD:/path`, `event:name`, or `cron:expr` |
| `run_id` | No | Supplied by orchestrator (output folder name) |
| `api_map_report.json` | No | B2 output when tracing HTTP |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Resolve entry point
Parse `entry_point_id`: `METHOD:/path`, `event:name`, or `cron:expression`.

Use B2 `api_map_report.json` when tracing HTTP endpoints.

## Phase 2 — Static call graph traversal
Walk calls max depth 20. Each step: `order`, `file_path`, `function_name`, `line`.

Classify `side_effects`: db_read, db_write, http_call, queue_publish.

List `external_dependencies` (DB, APIs, queues).

## Phase 3 — Diagram & uncertainties
Emit valid Mermaid `sequenceDiagram` in `sequence_diagram_mermaid`.

Record dynamic/reflection calls in `uncertainties`.

## Phase 4 — Write JSON output
`steps[0]` must be the entry point. Write `generated_projects/{run_id}/I2/output.json`.

---

## Eval deliverables

- Entry point
- Step-by-step path
- External deps
- Side effects
- Sequence diagram
- Uncertainties

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/I2/flow_trace_report.json`.

---

## Validation

- steps[0] is entry point
- All steps have file_path
- DC-I2-01 through DC-I2-04 pass

---

## Failure conditions

- INPUT_CONTRACT_VIOLATION: entry_point not found
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `I2` in output JSON
- [ ] Output written to `generated_projects/{run_id}/I2/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill I2 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill I2 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill I2
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`I2`

### Capability Level
`I`

### Time Budget
45 minutes

### Depends On
- B2

### Objective
Trace one endpoint, event, or cron job end-to-end from entry point to final DB/API/queue side effect.

### Inputs
- repository_path
- entry_point_id (METHOD:/path | event:name | cron:expression)
- api_map_report.json (B2, optional)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/I2/flow_trace_report.json`

```json
{
  "entry_point_id": "POST:/transactions",
  "entry_type": "endpoint",
  "external_dependencies": [],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "I",
  "scan_complete": true,
  "sequence_diagram_mermaid": "sequenceDiagram\n  Client->>Controller: POST /transactions",
  "side_effects": [
    "db_write:transactions"
  ],
  "steps": [
    {
      "file_path": "app/controllers/transaction.py",
      "function_name": "create",
      "line": 24
    }
  ],
  "task_id": "I2",
  "uncertainties": [],
  "warnings": []
}
```

### Eval Deliverables
- Entry point
- Step-by-step path
- External deps
- Side effects
- Sequence diagram
- Uncertainties

### Validation
- steps[0] is entry point
- All steps have file_path
- DC-I2-01 through DC-I2-04 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION: entry_point not found
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/intermediate/I2_flow_trace.skill.md`
- Eval blueprint: `eval_blueprints/I/I2_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I2_flow_trace_agent.md`


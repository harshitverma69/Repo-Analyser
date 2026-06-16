## Skill: Flow Trace

### Task ID
`I2`

### Level
`INTERMEDIATE`

### Objective
Trace one endpoint, event, or cron job end-to-end from entry point to final DB/API/queue side effect.

### Depends On
- B2

### Input Contract
```json
{
  "repository_path": "required",
  "entry_point_id": "required",
  "api_map_report.json": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/intermediate/I2_flow_trace_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill I2 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- steps[0] is entry point
- All steps have file_path
- DC-I2-01 through DC-I2-04 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION: entry_point not found
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/intermediate/I2_flow_trace.skill.md`
- Eval blueprint: `eval_blueprints/I/I2_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I2_flow_trace_agent.md`

### Sources
- Agent: `agents/intermediate/I2_flow_trace_agent.md`
- Blueprint: `eval_blueprints/I/I2_blueprint.md`
- Skill: `skills/intermediate/I2_flow_trace.skill.md`

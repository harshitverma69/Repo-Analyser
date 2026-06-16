## Skill: Api Endpoint Map

### Task ID
`B2`

### Level
`BASIC`

### Objective
Identify every externally exposed API route and frontend route; map each to handler and controller via static inspection.

### Depends On
- B1

### Input Contract
```json
{
  "repository_path": "required",
  "inventory_report.json": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/basics/B2_api_endpoint_map_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON + output.md via `python3 -m runtime.skill_finish write --run-id {run_id} --skill B2 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "controllers": [
    "TransactionController"
  ],
  "endpoints": [
    {
      "controller": "TransactionController",
      "handler_method": "create",
      "id": "POST:/transactions",
      "line": 24,
      "method": "POST",
      "request_dto": "TransactionRequest",
      "response_dto": "TransactionResponse",
      "route": "/transactions",
      "source_file": "app/controllers/transaction.py"
    }
  ],
  "frontend_routes": [],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "mapping": {
    "POST:/transactions": {
      "controller": "TransactionController",
      "handler": "create"
    }
  },
  "scan_complete": true,
  "task_id": "B2",
  "warnings": []
}
```

### Validation Rules
- Endpoint count matches unique (method, route) pairs
- Every endpoint has handler_method and source_file
- DC-B2-01 through DC-B2-04 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- ZERO_ARTIFACTS on known API repos
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/basics/B2_api_endpoint_map.skill.md`
- Eval blueprint: `eval_blueprints/B/B2_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B2_api_endpoint_map_agent.md`

### Sources
- Agent: `agents/basics/B2_api_endpoint_map_agent.md`
- Blueprint: `eval_blueprints/B/B2_blueprint.md`
- Skill: `skills/basics/B2_api_endpoint_map.skill.md`

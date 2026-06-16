## Skill: Polyglot Fastapi Node

### Task ID
`I4`

### Level
`INTERMEDIATE`

### Objective
Build FastAPI /convert service and Node.js CLI client with hardcoded rates, tests, and two-terminal README.

### Depends On
- B4
- B5

### Input Contract
```json
{
  "output_dir": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/intermediate/I4_polyglot_fastapi_node_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill I4 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- Both components run
- Integration script passes
- DC-I4-01 through DC-I4-02 pass

### Failure Conditions
- BUILD_FAILED
- INTEGRATION_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/intermediate/I4_polyglot_fastapi_node.skill.md`
- Eval blueprint: `eval_blueprints/I/I4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I4_polyglot_fastapi_node_agent.md`

### Sources
- Agent: `agents/intermediate/I4_polyglot_fastapi_node_agent.md`
- Blueprint: `eval_blueprints/I/I4_blueprint.md`
- Skill: `skills/intermediate/I4_polyglot_fastapi_node.skill.md`

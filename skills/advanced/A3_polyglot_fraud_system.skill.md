## Skill: Polyglot Fraud System

### Task ID
`A3`

### Level
`ADVANCED`

### Objective
Build mini fraud-score system: FastAPI ingestion, Node.js worker, Rust scoring engine with tests and README.

### Depends On
- B4
- B5
- B6
- I4

### Input Contract
```json
{
  "output_dir": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/advanced/A3_polyglot_fraud_system_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill A3 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- All 3 components build
- integration test passes
- DC-A3-01 through DC-A3-02 pass

### Failure Conditions
- BUILD_FAILED
- INTEGRATION_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/advanced/A3_polyglot_fraud_system.skill.md`
- Eval blueprint: `eval_blueprints/A/A3_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A3_polyglot_fraud_system_agent.md`

### Sources
- Agent: `agents/advanced/A3_polyglot_fraud_system_agent.md`
- Blueprint: `eval_blueprints/A/A3_blueprint.md`
- Skill: `skills/advanced/A3_polyglot_fraud_system.skill.md`

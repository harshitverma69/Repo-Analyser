## Skill: Fastapi Greenfield

### Task ID
`B4`

### Level
`BASIC`

### Objective
Build a small Python FastAPI service from scratch with POST/GET endpoints, input validation, tests, and README.

### Depends On
None

### Input Contract
```json
{
  "project_name": "required",
  "output_dir": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/basics/B4_fastapi_greenfield_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill B4 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- files_created includes main.py, requirements.txt, README.md, tests/
- tests.count >= 3
- run_proof.exit_code == 0
- DC-B4-01 through DC-B4-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/basics/B4_fastapi_greenfield.skill.md`
- Eval blueprint: `eval_blueprints/B/B4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B4_fastapi_greenfield_agent.md`

### Sources
- Agent: `agents/basics/B4_fastapi_greenfield_agent.md`
- Blueprint: `eval_blueprints/B/B4_blueprint.md`
- Skill: `skills/basics/B4_fastapi_greenfield.skill.md`

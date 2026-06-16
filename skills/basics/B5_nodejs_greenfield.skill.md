## Skill: Nodejs Greenfield

### Task ID
`B5`

### Level
`BASIC`

### Objective
Build equivalent transaction/balance service as Node.js API or CLI with tests and README.

### Depends On
- B4

### Input Contract
```json
{
  "project_name": "required",
  "output_dir": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/basics/B5_nodejs_greenfield_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill B5 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "endpoints_or_commands": [
    "POST /transactions",
    "GET /balance"
  ],
  "files_created": [
    "src/index.js",
    "package.json",
    "tests/api.test.js"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "mode": "api",
  "project_path": "generated_projects/example-run/B5/tx-node",
  "readme_commands": {
    "install": [
      "npm install"
    ],
    "run": [
      "npm start"
    ],
    "test": [
      "npm test"
    ]
  },
  "run_proof": {
    "command": "npm test",
    "exit_code": 0
  },
  "scan_complete": true,
  "task_id": "B5",
  "tests": {
    "command": "npm test",
    "count": 3,
    "exit_code": 0
  },
  "warnings": []
}
```

### Validation Rules
- tests.count >= 3
- run_proof.exit_code == 0
- DC-B5-01 through DC-B5-02 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/basics/B5_nodejs_greenfield.skill.md`
- Eval blueprint: `eval_blueprints/B/B5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B5_nodejs_greenfield_agent.md`

### Sources
- Agent: `agents/basics/B5_nodejs_greenfield_agent.md`
- Blueprint: `eval_blueprints/B/B5_blueprint.md`
- Skill: `skills/basics/B5_nodejs_greenfield.skill.md`

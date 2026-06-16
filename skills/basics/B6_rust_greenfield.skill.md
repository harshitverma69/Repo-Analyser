## Skill: Rust Greenfield

### Task ID
`B6`

### Level
`BASIC`

### Objective
Build Rust CLI that accepts file path, counts INFO/WARN/ERROR lines, handles missing file gracefully, with tests and README.

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
- Read agent spec: `agents/basics/B6_rust_greenfield_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON + output.md via `python3 -m runtime.skill_finish write --run-id {run_id} --skill B6 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "cli": {
    "accepts": "file_path",
    "counts": [
      "INFO",
      "WARN",
      "ERROR"
    ],
    "missing_file_exit_code": 1
  },
  "files_created": [
    "src/main.rs",
    "Cargo.toml",
    "tests/integration.rs"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "project_path": "generated_projects/example-run/B6/log-counter",
  "readme_commands": {
    "build": [
      "cargo build"
    ],
    "run": [
      "cargo run -- sample.log"
    ],
    "test": [
      "cargo test"
    ]
  },
  "run_proof": {
    "command": "cargo run -- sample.log",
    "exit_code": 0,
    "missing_file_proof": {
      "exit_code": 1
    }
  },
  "scan_complete": true,
  "task_id": "B6",
  "tests": {
    "command": "cargo test",
    "count": 3,
    "exit_code": 0
  },
  "warnings": []
}
```

### Validation Rules
- tests.count >= 3
- missing_file_proof exit graceful
- DC-B6-01 through DC-B6-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/basics/B6_rust_greenfield.skill.md`
- Eval blueprint: `eval_blueprints/B/B6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B6_rust_greenfield_agent.md`

### Sources
- Agent: `agents/basics/B6_rust_greenfield_agent.md`
- Blueprint: `eval_blueprints/B/B6_blueprint.md`
- Skill: `skills/basics/B6_rust_greenfield.skill.md`

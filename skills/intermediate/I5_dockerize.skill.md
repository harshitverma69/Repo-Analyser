## Skill: Dockerize

### Task ID
`I5`

### Level
`INTERMEDIATE`

### Objective
Containerize a service so it builds and runs cleanly in Docker with health check proof.

### Depends On
None

### Input Contract
```json
{
  "service_path": "required",
  "service_port": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/intermediate/I5_dockerize_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill I5 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "build_proof": {
    "command": "docker build -t tx-service .",
    "exit_code": 0
  },
  "dockerfile_path": "Dockerfile",
  "generated_at": "2026-06-16T12:00:00Z",
  "health_check": {
    "command": "curl -sf http://localhost:8080/health",
    "response_body_sample": {
      "status": "ok"
    },
    "response_status": 200
  },
  "level": "I",
  "readme_commands": {
    "build": [
      "docker build -t tx-service ."
    ],
    "curl_proof": [
      "curl http://localhost:8080/health"
    ],
    "run": [
      "docker run -p 8080:8080 tx-service"
    ]
  },
  "run_proof": {
    "command": "docker run -d -p 8080:8080 tx-service",
    "exit_code": 0
  },
  "scan_complete": true,
  "task_id": "I5",
  "warnings": []
}
```

### Validation Rules
- build_proof.exit_code == 0
- health_check.response_status == 200
- DC-I5-01 through DC-I5-02 pass

### Failure Conditions
- BUILD_FAILED
- RUN_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/intermediate/I5_dockerize.skill.md`
- Eval blueprint: `eval_blueprints/I/I5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I5_dockerize_agent.md`

### Sources
- Agent: `agents/intermediate/I5_dockerize_agent.md`
- Blueprint: `eval_blueprints/I/I5_blueprint.md`
- Skill: `skills/intermediate/I5_dockerize.skill.md`

## Skill: Docker Compose Stack

### Task ID
`D2`

### Level
`INFRA`

### Objective
Stand up multi-service stack (API + DB + worker) with docker-compose, seed data, and E2E test script.

### Depends On
- I5

### Input Contract
```json
{
  "output_dir": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/infra_devops/D2_docker_compose_stack_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON + output.md via `python3 -m runtime.skill_finish write --run-id {run_id} --skill D2 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "compose_file": "docker-compose.yml",
  "dockerfiles": [
    "api/Dockerfile",
    "worker/Dockerfile"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "inter_service_logs_proof": [
    "worker connected to api",
    "api wrote to postgres"
  ],
  "level": "D",
  "scan_complete": true,
  "seed_script": "scripts/seed.sql",
  "task_id": "D2",
  "teardown": {
    "command": "docker compose down -v",
    "reup_proof": {
      "exit_code": 0
    }
  },
  "test_run": {
    "command": "./scripts/e2e.sh",
    "exit_code": 0
  },
  "warnings": []
}
```

### Validation Rules
- test_run.exit_code == 0
- reup_proof.exit_code == 0
- DC-D2-01 through DC-D2-02 pass

### Failure Conditions
- COMPOSE_UP_FAILED
- E2E_TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/infra/D2_docker_compose_stack.skill.md`
- Eval blueprint: `eval_blueprints/D/D2_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D2_docker_compose_stack_agent.md`

### Sources
- Agent: `agents/infra_devops/D2_docker_compose_stack_agent.md`
- Blueprint: `eval_blueprints/D/D2_blueprint.md`
- Skill: `skills/infra/D2_docker_compose_stack.skill.md`

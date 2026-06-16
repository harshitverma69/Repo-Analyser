## Skill: Observability Bolt On

### Task ID
`D6`

### Level
`INFRA`

### Objective
Add structured logging and /metrics endpoint; stand up Prometheus + Grafana with working dashboard panel.

### Depends On
- I5

### Input Contract
```json
{
  "service_path": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/infra_devops/D6_observability_bolt_on_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill D6 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "code_diff_files": [
    "app/main.py",
    "app/metrics.py"
  ],
  "compose_stack": {
    "grafana": "docker-compose.observability.yml",
    "prometheus": "docker-compose.observability.yml"
  },
  "dashboard_panel": {
    "data_proof": {
      "series_points": 12
    },
    "query": "rate(http_requests_total[1m])",
    "title": "Request rate"
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "load_script": "scripts/load.sh",
  "metrics_endpoint": "/metrics",
  "readme_run_order": [
    "docker compose up -d",
    "bash scripts/load.sh",
    "open grafana :3000"
  ],
  "scan_complete": true,
  "task_id": "D6",
  "warnings": []
}
```

### Validation Rules
- /metrics returns prometheus format
- dashboard_panel has data
- DC-D6-01 through DC-D6-02 pass

### Failure Conditions
- METRICS_FAILED
- DASHBOARD_NO_DATA
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/infra/D6_observability_bolt_on.skill.md`
- Eval blueprint: `eval_blueprints/D/D6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D6_observability_bolt_on_agent.md`

### Sources
- Agent: `agents/infra_devops/D6_observability_bolt_on_agent.md`
- Blueprint: `eval_blueprints/D/D6_blueprint.md`
- Skill: `skills/infra/D6_observability_bolt_on.skill.md`

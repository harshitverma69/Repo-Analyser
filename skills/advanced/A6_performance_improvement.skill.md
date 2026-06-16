## Skill: Performance Improvement

### Task ID
`A6`

### Level
`ADVANCED`

### Objective
Find real performance bottleneck, make measurable minimal improvement, prove behavior unchanged.

### Depends On
None

### Input Contract
```json
{
  "service_path": "required",
  "benchmark_target": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/advanced/A6_performance_improvement_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill A6 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "after": {
    "improvement_pct": 54.2,
    "method": "hyperfine",
    "metric": "requests_per_sec",
    "value": 185
  },
  "baseline": {
    "method": "hyperfine",
    "metric": "requests_per_sec",
    "unit": "rps",
    "value": 120
  },
  "behavior_proof": {
    "exit_code": 0,
    "test_command": "pytest -q"
  },
  "change": {
    "description": "Use orjson dumps once per response",
    "files_changed": [
      "app/handlers.py"
    ]
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "A",
  "profiling": {
    "approach": "cProfile",
    "bottleneck": "JSON serialization in loop",
    "evidence": [
      "app/handlers.py:44"
    ]
  },
  "scan_complete": true,
  "task_id": "A6",
  "warnings": []
}
```

### Validation Rules
- after.value < baseline.value OR improvement_pct > 0
- behavior_proof.exit_code == 0
- DC-A6-01 through DC-A6-03 pass

### Failure Conditions
- BASELINE_FAILED
- NO_IMPROVEMENT
- BEHAVIOR_REGRESSION
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/advanced/A6_performance_improvement.skill.md`
- Eval blueprint: `eval_blueprints/A/A6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A6_performance_improvement_agent.md`

### Sources
- Agent: `agents/advanced/A6_performance_improvement_agent.md`
- Blueprint: `eval_blueprints/A/A6_blueprint.md`
- Skill: `skills/advanced/A6_performance_improvement.skill.md`

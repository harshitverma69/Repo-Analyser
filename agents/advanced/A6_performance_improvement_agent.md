---
name: cac-os-a6-performance-improvement
description: |
  CAC-OS A6 (ADVANCED) — Find real performance bottleneck, make measurable minimal improvement, prove behavior unchanged.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Performance Improvement (A6)

You are the **Performance Improvement** in the CAC-OS deterministic eval framework.

**Objective:** Find real performance bottleneck, make measurable minimal improvement, prove behavior unchanged.

**Capability level:** `A` · **Time budget:** 90 minutes · **Depends on:** None

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/A6/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service to profile |
| `benchmark_target` | Yes | Endpoint or function to measure |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Baseline measurement
Profile `benchmark_target` in `service_path` (latency, throughput, or CPU). Record `baseline`.

## Phase 2 — Targeted improvement
Apply minimal change addressing the real bottleneck (not premature optimization).

## Phase 3 — After measurement & behavior proof
Re-run benchmark → `after`. Run regression tests → `behavior_proof` with command + exit_code.

## Phase 4 — Write JSON output
Write `generated_projects/{run_id}/A6/output.json` showing measurable improvement.

---

## Eval deliverables

- Baseline numbers
- Profile results
- Bottleneck
- Targeted change
- After numbers
- Behavior proof

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/A6/performance_report.json`.

---

## Validation

- after.value < baseline.value OR improvement_pct > 0
- behavior_proof.exit_code == 0
- DC-A6-01 through DC-A6-03 pass

---

## Failure conditions

- BASELINE_FAILED
- NO_IMPROVEMENT
- BEHAVIOR_REGRESSION
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `A6` in output JSON
- [ ] Output written to `generated_projects/{run_id}/A6/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill A6 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill A6 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill A6
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`A6`

### Capability Level
`A`

### Time Budget
90 minutes

### Depends On
- None

### Objective
Find real performance bottleneck, make measurable minimal improvement, prove behavior unchanged.

### Inputs
- service_path (absolute path)
- benchmark_target (string)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/A6/performance_report.json`

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

### Eval Deliverables
- Baseline numbers
- Profile results
- Bottleneck
- Targeted change
- After numbers
- Behavior proof

### Validation
- after.value < baseline.value OR improvement_pct > 0
- behavior_proof.exit_code == 0
- DC-A6-01 through DC-A6-03 pass

### Failure Conditions
- BASELINE_FAILED
- NO_IMPROVEMENT
- BEHAVIOR_REGRESSION
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/advanced/A6_performance_improvement.skill.md`
- Eval blueprint: `eval_blueprints/A/A6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A6_performance_improvement_agent.md`


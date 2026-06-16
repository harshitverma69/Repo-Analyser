---
name: cac-os-d3-ci-pipeline
description: |
  CAC-OS D3 (INFRA) — Write CI workflow that lints, tests, builds and tags container image with green run proof.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Ci Pipeline (D3)

You are the **Ci Pipeline** in the CAC-OS deterministic eval framework.

**Objective:** Write CI workflow that lints, tests, builds and tags container image with green run proof.

**Capability level:** `D` · **Time budget:** 45 minutes · **Depends on:** `B3`, `I5`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/D3/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository to add CI to |
| `ci_platform` | Yes | `github_actions` or `gitlab_ci` |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — CI workflow
Write GitHub Actions or GitLab CI: lint, test, build, tag container image.

## Phase 2 — Green run proof
Trigger or simulate workflow; capture `pass_proof`. Optionally document `failure_demo` for a deliberate fail case.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/D3/output.json`.

---

## Eval deliverables

- Workflow YAML
- Cache/matrix
- Green run proof
- Failure mode demo

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/D3/ci_manifest.json`.

---

## Validation

- pass_proof.exit_code == 0
- failure_demo documents expected fail
- DC-D3-01 through DC-D3-02 pass

---

## Failure conditions

- WORKFLOW_INVALID
- PIPELINE_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `D3` in output JSON
- [ ] Output written to `generated_projects/{run_id}/D3/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill D3 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill D3 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill D3
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`D3`

### Capability Level
`D`

### Time Budget
45 minutes

### Depends On
- B3
- I5

### Objective
Write CI workflow that lints, tests, builds and tags container image with green run proof.

### Inputs
- repository_path
- ci_platform (github_actions|gitlab_ci)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/D3/ci_manifest.json`

```json
{
  "cache_config": {
    "pip": "~/.cache/pip"
  },
  "failure_demo": {
    "broken_commit": "bad1234",
    "expected_fail_stage": "test"
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "pass_proof": {
    "command_or_link": "act push",
    "exit_code": 0
  },
  "scan_complete": true,
  "task_id": "D3",
  "warnings": [],
  "workflow_file": ".github/workflows/ci.yml"
}
```

### Eval Deliverables
- Workflow YAML
- Cache/matrix
- Green run proof
- Failure mode demo

### Validation
- pass_proof.exit_code == 0
- failure_demo documents expected fail
- DC-D3-01 through DC-D3-02 pass

### Failure Conditions
- WORKFLOW_INVALID
- PIPELINE_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/infra/D3_ci_pipeline.skill.md`
- Eval blueprint: `eval_blueprints/D/D3_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D3_ci_pipeline_agent.md`


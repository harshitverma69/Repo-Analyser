---
name: repo-analyser-d1-terraform-plan
description: |
  Repo-Analyser D1 (INFRA) — Write Terraform for small service that passes validate and produces clean plan against test backend.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Terraform Plan (D1)

You are the **Terraform Plan** in the Repo-Analyser deterministic eval framework.

**Objective:** Write Terraform for small service that passes validate and produces clean plan against test backend.

**Capability level:** `D` · **Time budget:** 60 minutes · **Depends on:** None

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/D1/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Terraform output directory |
| `provider` | Yes | `aws` or `gcp` |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Terraform scaffold
Write `.tf` files under `output_dir` for small service (provider: aws or gcp input).

Include variables, outputs, minimal resources.

## Phase 2 — Validate & plan
Run `terraform validate` and `terraform plan` against test/local backend.

Record `validate_proof` and `plan_proof`.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/D1/output.json`.

---

## Eval deliverables

- .tf files
- Provider/backend
- validate output
- plan output
- README

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/D1/terraform_manifest.json`.

---

## Validation

- validate_proof.exit_code == 0
- plan_proof.exit_code == 0
- DC-D1-01 through DC-D1-02 pass

---

## Failure conditions

- VALIDATE_FAILED
- PLAN_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `D1` in output JSON
- [ ] Output written to `generated_projects/{run_id}/D1/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill D1 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill D1 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill D1
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`D1`

### Capability Level
`D`

### Time Budget
60 minutes

### Depends On
- None

### Objective
Write Terraform for small service that passes validate and produces clean plan against test backend.

### Inputs
- output_dir (absolute path)
- provider (aws|gcp)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/D1/terraform_manifest.json`

```json
{
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "plan_proof": {
    "changes_summary": {
      "add": 3,
      "change": 0,
      "destroy": 0
    },
    "command": "terraform plan",
    "exit_code": 0
  },
  "readme": {
    "apply": [
      "terraform apply -auto-approve"
    ],
    "destroy": [
      "terraform destroy -auto-approve"
    ]
  },
  "scan_complete": true,
  "task_id": "D1",
  "tf_files": [
    "main.tf",
    "variables.tf"
  ],
  "validate_proof": {
    "command": "terraform validate",
    "exit_code": 0
  },
  "variables": {
    "region": "us-east-1"
  },
  "warnings": []
}
```

### Eval Deliverables
- .tf files
- Provider/backend
- validate output
- plan output
- README

### Validation
- validate_proof.exit_code == 0
- plan_proof.exit_code == 0
- DC-D1-01 through DC-D1-02 pass

### Failure Conditions
- VALIDATE_FAILED
- PLAN_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/infra/D1_terraform_plan.skill.md`
- Eval blueprint: `eval_blueprints/D/D1_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D1_terraform_plan_agent.md`


---
name: repo-analyser-a1-multi-worktree-plan
description: |
  Repo-Analyser A1 (ADVANCED) — Split one feature/analysis task into parallel worktrees or agent sessions without merge chaos.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Multi Worktree Plan (A1)

You are the **Multi Worktree Plan** in the Repo-Analyser deterministic eval framework.

**Objective:** Split one feature/analysis task into parallel worktrees or agent sessions without merge chaos.

**Capability level:** `A` · **Time budget:** 45 minutes · **Depends on:** None

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/A1/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Git repository root |
| `task_description` | Yes | Feature or analysis to split |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Feature decomposition
Parse `task_description`. Identify independent slices that can run in parallel worktrees without file overlap.

## Phase 2 — Worktree plan
For each worktree: `name`, `branch`, `scope` (paths), `agent_session_notes`.

Define `merge_order` and conflict risk notes.

## Phase 3 — Write JSON output
Write `generated_projects/{run_id}/A1/output.json` — plan only, no git mutations in this task.

---

## Eval deliverables

- Task decomposition
- Worktree names
- Agent prompts
- Constraints
- Merge order
- Conflict plan

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/A1/worktree_plan.json`.

---

## Validation

- lanes have disjoint scopes
- merge_order defined
- DC-A1-01 through DC-A1-02 pass

---

## Failure conditions

- INPUT_CONTRACT_VIOLATION
- OVERLAPPING_LANE_SCOPE
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `A1` in output JSON
- [ ] Output written to `generated_projects/{run_id}/A1/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill A1 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill A1 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill A1
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`A1`

### Capability Level
`A`

### Time Budget
45 minutes

### Depends On
- None

### Objective
Split one feature/analysis task into parallel worktrees or agent sessions without merge chaos.

### Inputs
- repository_path
- task_description (string)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/A1/worktree_plan.json`

```json
{
  "agent_prompts": {
    "lane-api": "Implement POST /transactions only",
    "lane-worker": "Implement queue consumer only"
  },
  "conflict_plan": [
    "models/ may conflict \u2014 merge lane-api first"
  ],
  "decomposition": [
    {
      "lane_id": "lane-api",
      "scope": "API endpoints"
    },
    {
      "lane_id": "lane-worker",
      "scope": "Background worker"
    }
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "A",
  "merge_order": [
    "lane-api",
    "lane-worker"
  ],
  "scan_complete": true,
  "shared_constraints": [
    "Do not modify shared models without merge review"
  ],
  "task_id": "A1",
  "verification_plan": [
    "pytest -q after merge"
  ],
  "warnings": [],
  "worktrees": [
    {
      "lane_id": "lane-api",
      "name": "wt-lane-api-feature",
      "path": "../repo-wt-api"
    }
  ]
}
```

### Eval Deliverables
- Task decomposition
- Worktree names
- Agent prompts
- Constraints
- Merge order
- Conflict plan

### Validation
- lanes have disjoint scopes
- merge_order defined
- DC-A1-01 through DC-A1-02 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- OVERLAPPING_LANE_SCOPE
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/advanced/A1_multi_worktree_plan.skill.md`
- Eval blueprint: `eval_blueprints/A/A1_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A1_multi_worktree_plan_agent.md`


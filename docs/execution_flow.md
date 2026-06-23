# Execution Flow

## Single skill

1. `SkillOrchestrator.build_plan(run_id, skill_ids=[...])` → `ExecutionPlan`
2. `SkillRunner(run_id).run_plan(plan)` or `run_skill(skill)`
3. For each skill:
   - Validate input contract
   - Load golden reference from `generated_projects/_golden/{skill}/`
   - Normalize output (strip volatile keys, set `task_id`)
   - Validate output schema
   - Write `generated_projects/{run_id}/{skill}/output.json`
   - Export Markdown + optional CLI report

## Full pipeline

```bash
make run-pipeline RUN_ID=my-run
# equivalent:
python -m runtime --full-pipeline --run-id my-run
```

1. Orchestrator loads `core/skill_registry.json`
2. Computes transitive dependencies + topological order
3. Groups skills into parallel waves (independent deps)
4. Executes wave-by-wave; abort semantics controlled by `continue_on_failure`
5. Writes `execution_log.json` and `final_report.json` at run root

## DAG validation

```bash
make validate-dag
# exit 0 when acyclic, all deps registered, no orphans (informational)
```

## Determinism proof

```bash
make test-determinism
```

Runs pipeline twice; byte-compares all 24 `output.json` files.

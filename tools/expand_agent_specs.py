#!/usr/bin/env python3
"""Expand CAC-OS agent specs to full procedural detail (repo-structure-mapper style)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = ROOT / "generated_projects" / "_golden"
REGISTRY = json.loads((ROOT / "core" / "skill_registry.json").read_text(encoding="utf-8"))
TASKS = json.loads((ROOT / "scripts" / "task_registry.json").read_text(encoding="utf-8"))["tasks"]

COMMON_RULES = """
1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.
""".strip()

FINAL_STEP = """
## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill {task_id} --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill {task_id}
```
""".strip()


def _extract_section_text(text: str, heading: str) -> str:
    for prefix in ("###", "##"):
        pattern = rf"^{prefix} {re.escape(heading)}\s*\n(.*?)(?=\n(?:###|##) |\Z)"
        match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def _blueprint_text(task_id: str) -> str:
    level = TASKS[task_id]["level"]
    path = ROOT / "eval_blueprints" / level / f"{task_id}_blueprint.md"
    return path.read_text(encoding="utf-8")


def _checklist_lines(section: str) -> str:
    lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            lines.append(f"- {stripped[5:].strip()}")
        elif stripped.startswith("- "):
            lines.append(stripped)
    return "\n".join(lines) if lines else "- See eval blueprint."


def _golden_schema(task_id: str) -> str:
    output_file = TASKS[task_id]["output_file"]
    path = GOLDEN_DIR / task_id / output_file
    payload = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(payload, indent=2, sort_keys=True)


def _slug(task_id: str) -> str:
    return TASKS[task_id]["slug"]


def _agent_path(task_id: str) -> Path:
    meta = TASKS[task_id]
    folder = meta["folder"]
    slug = meta["slug"]
    return ROOT / "agents" / folder / f"{task_id}_{slug}_agent.md"


def _cursor_name(task_id: str) -> str:
    return f"cac-os-{task_id.lower()}-{_slug(task_id).replace('_', '-')}"


# Per-agent procedural phases (title + body markdown)
PHASES: dict[str, list[tuple[str, str]]] = {
    "B1": [
        (
            "Phase 1 — Repo reconnaissance",
            """
Before scanning symbols, establish context:

1. Read `README.md`, `package.json`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `pubspec.yaml`, `Cargo.toml`, `pyproject.toml`, or equivalent.
2. Note monorepo layout — list top-level apps/packages.
3. Record: repo name, languages, primary framework, build tool, architectural style if documented.
4. Identify source roots: `src/main/java`, `src/`, `lib/`, `app/`, `packages/*/src`, etc.
5. Exclude: `node_modules/`, `vendor/`, `build/`, `dist/`, `.git/`, `target/`, `coverage/`, `**/generated/**`, `*.g.dart`, `*.pb.go` (note generated code in `limitations` instead).
""",
        ),
        (
            "Phase 2 — Symbol discovery by category",
            """
Classify each **major** symbol into: `classes`, `interfaces`, `services`, `controllers`, `models`, `repositories`, `jobs`, `consumers`, `configurations`, `utilities`.

**Include** when exported/public, convention-named, referenced from multiple places, or clearly an entry point.

**Exclude** (unless user sets `includeTests: true`): test classes, mocks, trivial one-liners, auto-generated stubs.

Use stack-specific signals:

| Stack | Controllers | Services | Repositories | Models | Jobs | Consumers | Configs |
|-------|-------------|----------|--------------|--------|------|-----------|---------|
| Java/Spring | `@RestController`, `@Controller` | `@Service`, `*Service` | `@Repository`, `JpaRepository` | `@Entity`, `*Dto` | `@Scheduled`, Batch | `@KafkaListener` | `@Configuration` |
| TS/Node | `router.*`, `route.ts` | `*Service`, `services/` | `*Repository`, Prisma | Zod/Mongoose schemas | bull/cron in `jobs/` | Kafka/SQS listeners | `*.config.ts`, `config/` |
| Python | FastAPI `@router`, Django views | `*Service`, `services/` | `*Repository`, ORM | SQLAlchemy/Pydantic | Celery, `tasks.py` | queue consumers | `settings.py`, `config.py` |
| Flutter | — (use Cubit/Bloc) | `*Service` | `*Repository` | `*Model`, freezed | workmanager | stream/Firebase handlers | flavor configs |
| Go/Rust | `handlers/`, `api/` | `service/` | `store/` | `models/`, structs | cron in `jobs/` | NATS/Kafka | `config.go`, `config.rs` |

For each artifact capture: `name`, `file_path`, `language`, `evidence` (annotation or pattern matched).

Build `dependency_graph_summary` from import/require statements only (`nodes`, `edges` as `source->target` strings).

Populate `modules` with `{name, path}` for each major package/module directory.

Per-artifact fields in JSON (`artifacts.*[]` entries):

| Field | Description |
|-------|-------------|
| `name` | Class, interface, or module symbol name |
| `file_path` | Relative path from repo root |
| `language` | e.g. java, python, typescript |
| `evidence` | Annotation, suffix, or folder pattern matched |

Deduplicate by fully qualified name. If a symbol fits multiple categories, pick the **primary** role and note secondary in `evidence`.

#### Java / Kotlin / Spring Boot (extended)

| Category | Signals |
|----------|---------|
| Controllers | `@RestController`, `@Controller`, `@RequestMapping` |
| Services | `@Service`, `*Service`, `*ServiceImpl`, `service/` |
| Repositories | `@Repository`, `JpaRepository`, `CrudRepository`, `*Repository` |
| Models | `@Entity`, `@Table`, `*Dto`, `*Request`, `*Response`, records in `model/`, `entity/`, `dto/` |
| Interfaces | `interface` keyword, repository/service interfaces |
| Jobs | `@Scheduled`, Quartz `Job`, Spring Batch `*Tasklet`, `*Job` |
| Consumers | `@KafkaListener`, `@RabbitListener`, `@JmsListener`, `*Consumer`, `*Listener` |
| Configs | `@Configuration`, `@ConfigurationProperties`, `SecurityConfig`, `application.yml` |
| Utilities | `*Utils`, `*Helper`, `*Validator`, `util/`, `common/` |

#### JavaScript / TypeScript (extended)

| Category | Signals |
|----------|---------|
| Controllers | Express `router.*`, Next.js `route.ts`, API route files |
| Services | `*Service`, `services/`, RTK Query slices |
| Repositories | `*Repository`, `*Store`, Prisma/TypeORM, `dao/` |
| Models | Zod/Yup schemas, Mongoose schemas, `models/`, `types/` |
| Jobs | `node-cron`, bull/bullmq processors, `jobs/` |
| Consumers | Kafka/SQS/Rabbit in `consumers/`, `listeners/` |
| Configs | `config/`, `*.config.js/ts`, `next.config`, `vite.config` |
| Utilities | `utils/`, `helpers/`, `lib/`, validators |

#### Large repos

If any category exceeds **75** artifacts, group by package/module in `limitations` with per-subdirectory counts. Controllers, services, and repositories must remain fully listed; models/utilities may be summarized by directory when > 150.
""",
        ),
        (
            "Phase 3 — Layer & dependency overview",
            """
Summarize layer flow in `limitations` or module notes when useful:

- Controllers → services → repositories
- Consumers → services
- Central config wiring

Mark relationships as explicit (injection/import) or inferred (naming only) in `limitations` if ambiguous.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Set `files_scanned`, sort all artifact arrays by `name`, list `limitations` (excluded dirs, generated code, dynamic imports not resolved).

Write to `generated_projects/{run_id}/B1/output.json` matching the schema below.
""",
        ),
    ],
    "B2": [
        (
            "Phase 1 — Load context",
            """
Load `repository_path` and optional B1 `inventory_report.json` for controller/service hints.

Detect API framework: Spring MVC, FastAPI, Express, Gin, etc. from build files and imports.
""",
        ),
        (
            "Phase 2 — Backend route discovery",
            """
Extract every HTTP route via static inspection only:

| Framework | Where to look |
|-----------|-----------------|
| Spring | `@GetMapping`, `@PostMapping`, `@RequestMapping` on `@RestController` classes |
| FastAPI | `@router.get/post`, `APIRouter` includes, `app.get/post` |
| Express | `router.get/post`, `app.use` mount paths |
| Next.js | `app/api/**/route.ts`, `pages/api/**` |

For each endpoint record: `method`, `path` (full normalized path), `controller`, `handler_method`, `source_file`, `line`, `framework`.

Deduplicate by `(method, normalized_path)`.
""",
        ),
        (
            "Phase 3 — Frontend route discovery",
            """
Scan router configs: React Router, Next.js app dir, Vue router, Flutter go_router.

Record `frontend_routes`: `{path, source_file}`.

Build `mapping` object: route path → handler method name.
Populate `controllers` as sorted unique controller names.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Every endpoint must have `handler_method` and `source_file`. Write `generated_projects/{run_id}/B2/output.json`.
""",
        ),
    ],
    "B3": [
        (
            "Phase 1 — Framework detection",
            """
Scan for: `pytest.ini`, `pyproject.toml [tool.pytest]`, `jest.config.*`, `vitest.config.*`, `pom.xml` surefire, `Cargo.toml`, `build.gradle` test deps, `go test` layout.

Set `framework` to detected primary test runner (e.g. `pytest`, `jest`, `cargo test`, `junit`).
""",
        ),
        (
            "Phase 2 — Test file discovery",
            """
Collect test files by convention: `test_*.py`, `*_test.go`, `*.spec.ts`, `*Test.java`, `tests/**`.

If `module_path` input provided, scope discovery to that subtree.

List paths in `test_files` relative to repo root.
""",
        ),
        (
            "Phase 3 — Command execution",
            """
Define copy-paste commands in `commands`: `unit`, `integration`, `coverage`.

Run the primary unit command; populate `command_result` with `command`, `exit_code`, `stdout_hash`, `stderr_hash` (SHA256 first 16 hex chars).

If failures: list in `failures` and explain in `interpretation` with specific test names.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
`framework` non-empty when tests exist. Write `generated_projects/{run_id}/B3/output.json`.
""",
        ),
    ],
    "B4": [
        (
            "Phase 1 — Scaffold project",
            """
Create under `output_dir/{project_name}/`: `main.py` (FastAPI app), `requirements.txt`, `README.md`, `tests/`.

Required endpoints: `POST /transactions`, `GET /transactions`, `GET /balance`.
Use Pydantic models for request/response validation.
""",
        ),
        (
            "Phase 2 — Tests",
            """
Add minimum 3 pytest tests (validation errors, happy path, balance logic).

Record in manifest: `tests.count`, `tests.files`, `tests.command`, `tests.exit_code`.
""",
        ),
        (
            "Phase 3 — Run proof",
            """
Start app via TestClient or uvicorn; capture `run_proof`: `command`, `exit_code`, `response_sample`.

Document install/run/test in `readme_commands`.
""",
        ),
        (
            "Phase 4 — Write JSON manifest",
            """
List all `files_created`, `endpoints`, proofs. Write `generated_projects/{run_id}/B4/output.json`.
""",
        ),
    ],
    "B5": [
        (
            "Phase 1 — Scaffold Node service",
            """
Create transaction/balance API or CLI under `output_dir/{project_name}/` with `package.json`, entry file, README.

Parity with B4 domain: POST/GET transactions, GET balance (or CLI equivalents).
""",
        ),
        (
            "Phase 2 — Tests & proof",
            """
Add tests (jest/vitest/node:test). Run test command; record exit code.

Provide `run_proof` with sample request/response or CLI output.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/B5/output.json` with `files_created`, `tests`, `readme_commands`, `run_proof`.
""",
        ),
    ],
    "B6": [
        (
            "Phase 1 — Scaffold Rust CLI",
            """
Create Cargo project under `output_dir/{project_name}/` that accepts a file path argument.

Count lines containing INFO, WARN, ERROR (case-sensitive or documented rules).
""",
        ),
        (
            "Phase 2 — Error handling & tests",
            """
Handle missing file gracefully (non-zero exit, clear message).

Add unit/integration tests; include `missing_file_proof` in manifest.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/B6/output.json` with `files_created`, `tests`, `run_proof`, `missing_file_proof`.
""",
        ),
    ],
    "I1": [
        (
            "Phase 1 — ORM / schema discovery",
            """
Detect ORM: SQLAlchemy, Django ORM, JPA/Hibernate, Prisma, TypeORM, Mongoose.

Scan model/entity files for table definitions.
""",
        ),
        (
            "Phase 2 — Tables & relationships",
            """
For each table: `table_name`, `entity_name`, `file_path`, `columns`, `source_citation`.

Extract relationships: FK, `@OneToMany`, `@ManyToOne`, etc.

Generate valid `mermaid_er` diagram string.
""",
        ),
        (
            "Phase 3 — Write JSON output",
            """
Every table cites source file. Write `generated_projects/{run_id}/I1/output.json`.
""",
        ),
    ],
    "I2": [
        (
            "Phase 1 — Resolve entry point",
            """
Parse `entry_point_id`: `METHOD:/path`, `event:name`, or `cron:expression`.

Use B2 `api_map_report.json` when tracing HTTP endpoints.
""",
        ),
        (
            "Phase 2 — Static call graph traversal",
            """
Walk calls max depth 20. Each step: `order`, `file_path`, `function_name`, `line`.

Classify `side_effects`: db_read, db_write, http_call, queue_publish.

List `external_dependencies` (DB, APIs, queues).
""",
        ),
        (
            "Phase 3 — Diagram & uncertainties",
            """
Emit valid Mermaid `sequenceDiagram` in `sequence_diagram_mermaid`.

Record dynamic/reflection calls in `uncertainties`.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
`steps[0]` must be the entry point. Write `generated_projects/{run_id}/I2/output.json`.
""",
        ),
    ],
    "I3": [
        (
            "Phase 1 — Scope the change",
            """
Read `change_spec`: description + target module. Load B3 test commands for the module.

Plan minimal diff — no drive-by refactors.
""",
        ),
        (
            "Phase 2 — Implement & update tests",
            """
Apply focused change. Update or add tests covering the change.

Record files touched and diff summary.
""",
        ),
        (
            "Phase 3 — Verification",
            """
Run tests; populate `test_result` and `verification_log` (agent_suggested, manually_verified, uncertain).
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Write `generated_projects/{run_id}/I3/output.json`.
""",
        ),
    ],
    "I4": [
        (
            "Phase 1 — FastAPI /convert service",
            """
Build currency conversion API (hardcoded rates) under `output_dir` with tests.
""",
        ),
        (
            "Phase 2 — Node CLI client",
            """
Build Node client that calls the FastAPI service; document two-terminal README workflow.
""",
        ),
        (
            "Phase 3 — Integration proof",
            """
Run both; record integration test proof in manifest.
""",
        ),
        (
            "Phase 4 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/I4/output.json` with `fastapi_service`, `node_client`, proofs.
""",
        ),
    ],
    "I5": [
        (
            "Phase 1 — Dockerfile & context",
            """
Write multi-stage or slim Dockerfile for `service_path`. Expose `service_port`.

Add `.dockerignore` if missing.
""",
        ),
        (
            "Phase 2 — Build & run",
            """
`docker build` and `docker run` with health check endpoint.

Record `build_proof` and `health_check` with commands and exit codes.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/I5/output.json`.
""",
        ),
    ],
    "I6": [
        (
            "Phase 1 — Reproduce bug",
            """
Use `bug_context` symptoms and hints. Run reproduction steps; capture logs/errors.
""",
        ),
        (
            "Phase 2 — Root cause analysis",
            """
Trace with I2-style static analysis if needed. Identify file paths and lines for root cause.
""",
        ),
        (
            "Phase 3 — Minimal fix & verify",
            """
Apply smallest correct fix. Run verification commands; populate `verification` log.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Write `generated_projects/{run_id}/I6/output.json` with root cause, fix, and proof.
""",
        ),
    ],
    "A1": [
        (
            "Phase 1 — Feature decomposition",
            """
Parse `task_description`. Identify independent slices that can run in parallel worktrees without file overlap.
""",
        ),
        (
            "Phase 2 — Worktree plan",
            """
For each worktree: `name`, `branch`, `scope` (paths), `agent_session_notes`.

Define `merge_order` and conflict risk notes.
""",
        ),
        (
            "Phase 3 — Write JSON output",
            """
Write `generated_projects/{run_id}/A1/output.json` — plan only, no git mutations in this task.
""",
        ),
    ],
    "A2": [
        (
            "Phase 1 — Create worktrees",
            """
Load A1 `worktree_plan.json`. Create two parallel git worktrees per plan.
""",
        ),
        (
            "Phase 2 — Independent changes",
            """
Implement scoped changes in each worktree. Run tests in each.
""",
        ),
        (
            "Phase 3 — Reconcile & merge",
            """
Merge or rebase per plan. Resolve conflicts; record in `conflicts` array.

Final `test_result` must pass on integrated branch.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Write `generated_projects/{run_id}/A2/output.json`.
""",
        ),
    ],
    "A3": [
        (
            "Phase 1 — FastAPI ingestion service",
            """
Transaction ingestion API with validation and persistence stub.
""",
        ),
        (
            "Phase 2 — Node worker + Rust scoring engine",
            """
Node.js worker consumes/processes events; Rust engine computes fraud score.
""",
        ),
        (
            "Phase 3 — Integration tests & README",
            """
End-to-end test across three components. Document architecture in README.
""",
        ),
        (
            "Phase 4 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/A3/output.json` with component paths and `tests.integration` proof.
""",
        ),
    ],
    "A4": [
        (
            "Phase 1 — Modernization scan",
            """
Load B1 inventory and B3 test commands. Identify debt: outdated deps, missing tests, anti-patterns.
""",
        ),
        (
            "Phase 2 — Prioritize & implement first step",
            """
Rank findings by value/risk. Implement exactly one executable first step (smallest high-value change).
""",
        ),
        (
            "Phase 3 — Verification",
            """
Run tests; record before/after in `first_step` and `verification`.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Write `generated_projects/{run_id}/A4/output.json`.
""",
        ),
    ],
    "A5": [
        (
            "Phase 1 — Load diff",
            """
Obtain `diff_or_pr_ref` against `repository_path`. Parse changed files and hunks.
""",
        ),
        (
            "Phase 2 — Adversarial review",
            """
For each issue assign:

| Category | Look for |
|----------|----------|
| correctness | logic bugs, edge cases, wrong types |
| security | injection, secrets, auth bypass |
| test | missing coverage, brittle tests |
| performance | N+1, unbounded loops, sync I/O |
| maintainability | duplication, unclear naming, hardcoded paths |

Severity: `blocking` or `non_blocking`. Every issue needs `file_path`, `line`, `description`, `suggested_fix`, `verification_steps[]`.
""",
        ),
        (
            "Phase 3 — Write JSON output",
            """
Write `generated_projects/{run_id}/A5/output.json`. Blocking issues must have actionable fixes.
""",
        ),
    ],
    "A6": [
        (
            "Phase 1 — Baseline measurement",
            """
Profile `benchmark_target` in `service_path` (latency, throughput, or CPU). Record `baseline`.
""",
        ),
        (
            "Phase 2 — Targeted improvement",
            """
Apply minimal change addressing the real bottleneck (not premature optimization).
""",
        ),
        (
            "Phase 3 — After measurement & behavior proof",
            """
Re-run benchmark → `after`. Run regression tests → `behavior_proof` with command + exit_code.
""",
        ),
        (
            "Phase 4 — Write JSON output",
            """
Write `generated_projects/{run_id}/A6/output.json` showing measurable improvement.
""",
        ),
    ],
    "D1": [
        (
            "Phase 1 — Terraform scaffold",
            """
Write `.tf` files under `output_dir` for small service (provider: aws or gcp input).

Include variables, outputs, minimal resources.
""",
        ),
        (
            "Phase 2 — Validate & plan",
            """
Run `terraform validate` and `terraform plan` against test/local backend.

Record `validate_proof` and `plan_proof`.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/D1/output.json`.
""",
        ),
    ],
    "D2": [
        (
            "Phase 1 — Compose stack",
            """
Create `docker-compose.yml`: API + DB + worker. Seed data script. E2E test script.
""",
        ),
        (
            "Phase 2 — Run E2E",
            """
`docker compose up`, run E2E script, tear down cleanly.

Record `test_run` and `teardown` proofs.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/D2/output.json`.
""",
        ),
    ],
    "D3": [
        (
            "Phase 1 — CI workflow",
            """
Write GitHub Actions or GitLab CI: lint, test, build, tag container image.
""",
        ),
        (
            "Phase 2 — Green run proof",
            """
Trigger or simulate workflow; capture `pass_proof`. Optionally document `failure_demo` for a deliberate fail case.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/D3/output.json`.
""",
        ),
    ],
    "D4": [
        (
            "Phase 1 — K8s manifests",
            """
Deployment, Service, ConfigMap/Secret as needed for `service_path`.
""",
        ),
        (
            "Phase 2 — Validate & deploy",
            """
`kubectl apply --dry-run=client` or kubeval. Deploy to kind/minikube.

`curl_proof` against service endpoint.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/D4/output.json`.
""",
        ),
    ],
    "D5": [
        (
            "Phase 1 — Bootstrap mechanism",
            """
Choose `bootstrap_type`: devcontainer, nix, or makefile+mise. Single command from fresh clone.
""",
        ),
        (
            "Phase 2 — Clean-machine proof",
            """
Document and run bootstrap + tests on clean environment simulation.

Record `bootstrap_proof` and `test_proof`.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Write `generated_projects/{run_id}/D5/output.json`.
""",
        ),
    ],
    "D6": [
        (
            "Phase 1 — Instrument service",
            """
Add structured logging and `/metrics` (Prometheus format) to `service_path`.
""",
        ),
        (
            "Phase 2 — Observability stack",
            """
Prometheus scrape config + Grafana dashboard with at least one working panel.
""",
        ),
        (
            "Phase 3 — Write JSON manifest",
            """
Record `dashboard_panel` proof (screenshot hash or query result). Write `generated_projects/{run_id}/D6/output.json`.
""",
        ),
    ],
}

INPUTS: dict[str, str] = {
    "B1": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Absolute path to repository root |
| `run_id` | No | Output folder name (orchestrator supplies; default: repo slug) |
| `scope` | No | Subdirectory or module to limit scan |
| `includeTests` | No | Default `false` — skip test directories |""",
    "B2": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `run_id` | No | Supplied by orchestrator (output folder name) |
| `inventory_report.json` | No | B1 output for controller hints |""",
    "B3": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `run_id` | No | Supplied by orchestrator (output folder name) |
| `module_path` | No | Limit discovery to a module subtree |""",
    "B4": """| Field | Required | Description |
|-------|----------|-------------|
| `project_name` | Yes | New project directory name |
| `output_dir` | Yes | Absolute path for greenfield output |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "B5": """| Field | Required | Description |
|-------|----------|-------------|
| `project_name` | Yes | New project directory name |
| `output_dir` | Yes | Absolute path for greenfield output |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "B6": """| Field | Required | Description |
|-------|----------|-------------|
| `project_name` | Yes | Cargo project name |
| `output_dir` | Yes | Absolute path for greenfield output |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "I1": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `run_id` | No | Supplied by orchestrator (output folder name) |
| `inventory_report.json` | No | B1 output |""",
    "I2": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `entry_point_id` | Yes | `METHOD:/path`, `event:name`, or `cron:expr` |
| `run_id` | No | Supplied by orchestrator (output folder name) |
| `api_map_report.json` | No | B2 output when tracing HTTP |""",
    "I3": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `change_spec` | Yes | `{description, target_module}` |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "I4": """| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Absolute path for both services |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "I5": """| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service root to containerize |
| `service_port` | Yes | Exposed port integer |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "I6": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `bug_context` | Yes | `{symptoms, reproduction_hint}` |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "A1": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Git repository root |
| `task_description` | Yes | Feature or analysis to split |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "A2": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Git repository root |
| `worktree_plan.json` | Yes | A1 output |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "A3": """| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Absolute path for fraud system |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "A4": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `inventory_report.json` | Yes | B1 output |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "A5": """| Field | Required | Description |
|-------|----------|-------------|
| `diff_or_pr_ref` | Yes | Diff, commit range, or PR reference |
| `repository_path` | Yes | Repository root |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "A6": """| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service to profile |
| `benchmark_target` | Yes | Endpoint or function to measure |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "D1": """| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Terraform output directory |
| `provider` | Yes | `aws` or `gcp` |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "D2": """| Field | Required | Description |
|-------|----------|-------------|
| `output_dir` | Yes | Stack output directory |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "D3": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository to add CI to |
| `ci_platform` | Yes | `github_actions` or `gitlab_ci` |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "D4": """| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service to deploy |
| `cluster` | Yes | `kind` or `minikube` |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "D5": """| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `bootstrap_type` | Yes | `devcontainer`, `nix`, or `makefile_mise` |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
    "D6": """| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service to instrument |
| `run_id` | No | Supplied by orchestrator (output folder name) |""",
}


INPUT_BULLETS: dict[str, list[str]] = {
    "B1": ["repository_path (absolute string)"],
    "B2": ["repository_path", "inventory_report.json (from B1, optional)"],
    "B3": ["repository_path", "module_path (optional string)"],
    "B4": ["project_name (string)", "output_dir (absolute path)"],
    "B5": ["project_name (string)", "output_dir (absolute path)"],
    "B6": ["project_name (string)", "output_dir (absolute path)"],
    "I1": ["repository_path", "inventory_report.json (B1, optional)"],
    "I2": ["repository_path", "entry_point_id (METHOD:/path | event:name | cron:expression)", "api_map_report.json (B2, optional)"],
    "I3": ["repository_path", "change_spec {description, target_module}"],
    "I4": ["output_dir (absolute path)"],
    "I5": ["service_path (absolute path)", "service_port (integer)"],
    "I6": ["repository_path", "bug_context {symptoms, reproduction_hint}"],
    "A1": ["repository_path", "task_description (string)"],
    "A2": ["repository_path", "worktree_plan.json (A1)"],
    "A3": ["output_dir (absolute path)"],
    "A4": ["repository_path", "inventory_report.json (B1)"],
    "A5": ["diff_or_pr_ref (string)", "repository_path"],
    "A6": ["service_path (absolute path)", "benchmark_target (string)"],
    "D1": ["output_dir (absolute path)", "provider (aws|gcp)"],
    "D2": ["output_dir (absolute path)"],
    "D3": ["repository_path", "ci_platform (github_actions|gitlab_ci)"],
    "D4": ["service_path (absolute path)", "cluster (kind|minikube)"],
    "D5": ["repository_path", "bootstrap_type (devcontainer|nix|makefile_mise)"],
    "D6": ["service_path (absolute path)"],
}


def _display_name(task_id: str, slug: str) -> str:
    parts = slug.split("_")
    if parts and parts[-1] == "agent":
        parts = parts[:-1]
    if parts and parts[0].upper() == task_id:
        parts = parts[1:]
    return " ".join(part.replace("-", " ").title() for part in parts) if parts else slug


def render_agent(task_id: str) -> str:
    meta = REGISTRY["skills"][task_id]
    task_meta = TASKS[task_id]
    blueprint = _blueprint_text(task_id)
    json_schema = _golden_schema(task_id)
    time_budget = _extract_section_text(blueprint, "Time Budget") or "see blueprint"
    validation = _checklist_lines(_extract_section_text(blueprint, "Success Criteria"))
    failure = _checklist_lines(_extract_section_text(blueprint, "Failure Conditions"))
    eval_deliverables = _checklist_lines(_extract_section_text(blueprint, "Deliverables Checklist"))
    depends = meta.get("depends_on") or []
    depends_text = ", ".join(f"`{d}`" for d in depends) if depends else "None"
    level = meta.get("level", task_meta["level"])
    display_name = _display_name(task_id, task_meta["slug"])
    description = meta["description"]
    output_file = task_meta["output_file"]
    slug = task_meta["slug"]

    phases_md = ""
    for title, body in PHASES.get(task_id, []):
        phases_md += f"\n## {title}\n{body.strip()}\n"

    checklist_items = [
        f"`task_id` is `{task_id}` in output JSON",
        f"Output written to `generated_projects/{{run_id}}/{task_id}/output.json`",
        "`generated_at` set (ISO 8601 UTC)",
        "All required proof fields populated with real command results",
        f"python3 -m runtime.skill_finish write --run-id <run_id> --skill {task_id} executed as final step",
    ]
    if task_id == "B1":
        checklist_items.extend(
            [
                "Every artifact has `file_path` evidence",
                "All ten artifact categories present (empty arrays allowed)",
                "Category counts consistent with `artifacts` contents",
                "`dependency_graph_summary` built from imports only",
            ]
        )

    checklist = "\n".join(f"- [ ] {item}" for item in checklist_items)

    input_bullets = "\n".join(f"- {item}" for item in INPUT_BULLETS.get(task_id, []))
    depends_on_section = "\n".join(f"- {d}" for d in depends) if depends else "- None"

    return f"""---
name: {_cursor_name(task_id)}
description: |
  CAC-OS {task_id} ({level}) — {description}
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: {display_name} ({task_id})

You are the **{display_name}** in the CAC-OS deterministic eval framework.

**Objective:** {description}

**Capability level:** `{task_meta['level']}` · **Time budget:** {time_budget} · **Depends on:** {depends_text}

Your primary deliverable is **strict JSON** at `generated_projects/{{run_id}}/{task_id}/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

{INPUTS.get(task_id, "| Field | Required | Description |\\n|-------|----------|-------------|\\n| See agent spec | — | — |")}

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

{phases_md.strip()}

---

## Eval deliverables

{eval_deliverables or "_See phases above._"}

---

## Rules

{COMMON_RULES}

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/{task_id}/{output_file}`.

---

## Validation

{validation or "_See eval blueprint._"}

---

## Failure conditions

{failure or "_See eval blueprint._"}

---

## Completion checklist

{checklist}

---

{FINAL_STEP.format(task_id=task_id)}

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`{task_id}`

### Capability Level
`{task_meta['level']}`

### Time Budget
{time_budget}

### Depends On
{depends_on_section}

### Objective
{description}

### Inputs
{input_bullets}

### Outputs (STRICT JSON)
Output file: `generated_projects/{{run_id}}/{task_id}/{output_file}`

```json
{json_schema}
```

### Eval Deliverables
{eval_deliverables or "- See phases above."}

### Validation
{validation or "- See eval blueprint."}

### Failure Conditions
{failure or "- See eval blueprint."}

---

## References

- Skill spec: `{meta['path']}`
- Eval blueprint: `eval_blueprints/{task_meta['level']}/{task_id}_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/{task_meta['folder']}/{task_id}_{slug}_agent.md`
"""


def main() -> int:
    updated: list[str] = []
    for task_id in sorted(REGISTRY["skills"].keys(), key=lambda t: (t[0], int(t[1:]))):
        path = _agent_path(task_id)
        if not path.is_file():
            print(f"SKIP {task_id}: missing {path}", file=__import__("sys").stderr)
            continue
        content = render_agent(task_id)
        path.write_text(content + "\n", encoding="utf-8")
        updated.append(task_id)
    print(f"Expanded {len(updated)} agent specs: {', '.join(updated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

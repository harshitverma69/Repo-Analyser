"""Reporting metadata and skill title registry."""

from __future__ import annotations

from dataclasses import dataclass

SKILL_TITLES: dict[str, str] = {
    "B1": "Repo Artifact Inventory",
    "B2": "API Endpoint Map",
    "B3": "Test Discovery",
    "B4": "FastAPI Greenfield",
    "B5": "Node.js Greenfield",
    "B6": "Rust Greenfield CLI",
    "I1": "ER Diagram",
    "I2": "Flow Trace",
    "I3": "Safe Change",
    "I4": "Polyglot FastAPI + Node",
    "I5": "Dockerize",
    "I6": "Bug Diagnosis",
    "A1": "Multi-Worktree Plan",
    "A2": "Parallel Worktrees Execute",
    "A3": "Polyglot Fraud System",
    "A4": "Modernization",
    "A5": "Adversarial Code Review",
    "A6": "Performance Improvement",
    "D1": "Terraform Plan",
    "D2": "Docker Compose Stack",
    "D3": "CI Pipeline",
    "D4": "Kubernetes Manifests",
    "D5": "Reproducible Dev Environment",
    "D6": "Observability Bolt-On",
}


@dataclass(frozen=True)
class ReportMetadata:
    run_id: str
    skill_id: str
    task_id: str
    level: str

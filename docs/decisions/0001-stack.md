# ADR 0001 — Backend stack: Python 3.12, uv, FastAPI, Docker

Date: 2026-09 · Status: accepted

## Context
The course project needs a small HTTP service that agents will extend across several modules.
It must be trivially testable without network and runnable identically on a laptop and a VPS.

## Decision
- Python 3.12 with `uv` for environments and `ruff` for lint.
- FastAPI as a thin adapter; domain logic in plain modules with no framework imports.
- One Docker image per service, wired by a root `compose.yaml`.

## Consequences
- Domain tests run in milliseconds and need no dependencies beyond pytest.
- Agents get a stable target ("make test", "docker-check") instead of ad-hoc commands.
- Adding a service means copying the layout, not inventing one.

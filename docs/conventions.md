# Conventions

## Layout

```
apps/backend/
  src/dice_api/dice/    pure domain: parser.py, roller.py — no HTTP, no I/O
  src/dice_api/main.py  FastAPI adapter: validation, serialisation, error mapping
  tests/                pytest; domain tests do not import FastAPI
```

Future services follow the same shape (`apps/<name>/src/<pkg>/`), and every CLI lives in `tools/<name>/`.

## Python

- 3.12; `uv venv` + `uv pip install -e ".[dev]"`; `ruff` (`make lint`), line length 110.
- Dataclasses for domain values (`frozen=True, slots=True`); pydantic models only at the HTTP edge.
- Type hints on all public functions. `from __future__ import annotations` at the top of every module.
- Public functions have a one-paragraph docstring saying what they guarantee, not how they work.

## Errors

- Domain raises `ValueError` with an actionable message: what was wrong and what is expected
  (`"keep count must be between 1 and 4 (got 5)"`).
- The HTTP layer maps `ValueError` → 422 with the same message in `detail`. Nothing else is caught.

## API

- GET with query params for read-only operations; JSON bodies for commands (later modules).
- Every random result includes `seed`; passing the same `seed` back replays the result exactly.
- Limits are explicit constants (`MAX_COUNT`, `MAX_SIDES`) and exposed at `/limits`.

## Git

- Conventional Commits; imperative subject ≤ 72 chars; body explains *why*.
- One logical change per commit. Tests and the code they cover go in the same commit.
- Agents never push. Humans review and push.

## Decisions

Structural choices get an ADR in `docs/decisions/NNNN-title.md` (context, decision, consequences).

# Module 01 — code snapshot

New in this module (compared with 00-code, which was a separate mini-agent package):

- Monorepo layout: `apps/backend` (FastAPI `dice-api`), `docs/`, `.opencode/`, `compose.yaml`, `Makefile`.
- `AGENTS.md` v1: constitution (7 rules) + working agreements + map. `docs/conventions.md` with details.
- `opencode.json`: permission policy (allow-list of safe commands, deny-list of destructive ones).
- `.opencode/agent/reviewer.md` (read-only subagent), `.opencode/command/{test,check,review}.md`,
  `.opencode/skills/{test-first,docker-check}`.
- Backend domain: `dice/parser.py` (reference solution of the module-00 practicum), `dice/roller.py`
  (seeded, replayable); HTTP: `/health`, `/parse`, `/roll`, `/limits`. 31 tests.
- `docs/experiments/01-permissions.md` + three permission profiles for the autonomy experiment.
- `docs/decisions/0001-stack.md` — first ADR.

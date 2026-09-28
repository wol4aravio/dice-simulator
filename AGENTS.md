# dice-course — instructions for coding agents

You are working in a monorepo for a dice-roll simulator (course project).
Read this file fully; read `docs/conventions.md` before touching code; read a
skill's `SKILL.md` before using it. Keep this file short — details live in `docs/`.

## Constitution (non-negotiable)

1. **Tests first, tests always.** No behaviour change without a test that fails before and passes after. Run `make test` before you report done.
2. **Docker-first.** Every service runs via `compose.yaml`. If it works only on your machine, it does not work.
3. **Pure domain, thin edges.** Business logic lives in plain Python modules with no I/O (`apps/backend/src/dice_api/dice/`). HTTP, CLI and storage are thin adapters over it.
4. **Reproducibility.** Anything random carries its seed in the output so it can be replayed exactly.
5. **JSON out.** Every CLI we build emits JSON on stdout and diagnostics on stderr, with a `--dry-run` where side effects exist.
6. **Secrets only from the environment.** Never write a key into a file that is committed. `.env` is gitignored; `.env.example` documents the keys.
7. **Never push, never force.** `git push`, `git push --force`, `git reset --hard` are for the human.

## Working agreements

- Python 3.12, `uv` for environments, `ruff` for lint/format (line length 110). Type hints on every public function.
- Errors: raise `ValueError` with an *actionable* message in the domain; map to HTTP 422 at the edge. Never swallow exceptions.
- Commits: Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`), one logical change per commit.
- Do not guess library APIs. Check the installed version (`uv pip show <pkg>`) or read the source in `.venv/`.
- When a task is ambiguous, state your assumption in one line and proceed; do not stop to ask.
- After changing code: `make test`. After changing a Dockerfile or compose: use the `docker-check` skill.

## Map

| Path | What |
|---|---|
| `apps/backend/` | FastAPI service `dice-api`; domain in `src/dice_api/dice/`, HTTP in `src/dice_api/main.py`, tests in `tests/` |
| `docs/conventions.md` | code conventions in detail |
| `docs/decisions/` | architecture decision records (ADR); add one when you make a structural choice |
| `.opencode/skills/` | skills: `test-first`, `docker-check` |
| `.opencode/command/` | slash commands: `/test`, `/check`, `/review` |
| `.opencode/agent/` | `reviewer` — read-only review subagent |

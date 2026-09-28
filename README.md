# dice-course

Monorepo of the course project — a dice-roll simulator built with coding agents.
Module 01 snapshot: backend skeleton + agent configuration.

```bash
cd apps/backend && uv venv && source .venv/bin/activate && uv pip install -e ".[dev]" && cd ../..
make test            # 31 tests
make up              # http://127.0.0.1:8000/docs
opencode             # in the repo root: AGENTS.md, opencode.json and .opencode/ are picked up
```

See `AGENTS.md` (what agents must know), `docs/conventions.md` (how we write code),
`docs/experiments/01-permissions.md` (the autonomy experiment of module 01).

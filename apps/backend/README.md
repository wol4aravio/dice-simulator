# dice-api

Backend of the dice simulator. Module 01 skeleton: `/health`, `/parse`, `/roll`, `/limits`.

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uv run pytest -q
uv run uvicorn dice_api.main:app --reload     # http://127.0.0.1:8000/docs
```

Layout: `src/dice_api/dice/` is the pure domain (parser, roller) — no HTTP, fully unit-tested;
`src/dice_api/main.py` is the thin FastAPI layer.

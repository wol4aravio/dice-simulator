"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="Dice Simulator API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the API is ready to accept roll requests."""
    return {"status": "ok"}

"""HTTP layer. Thin on purpose: validation, serialisation, error mapping.

Run locally:   uv run uvicorn dice_api.main:app --reload
In Docker:     docker compose up backend
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from . import __version__
from .dice import MAX_COUNT, MAX_SIDES, RollResult, parse, roll

app = FastAPI(title="Dice API", version=__version__)


class RollResponse(BaseModel):
    expression: str = Field(examples=["3d6+2"])
    seed: int
    rolls: list[int]
    kept: list[int]
    dropped: list[int]
    modifier: int
    total: int

    @classmethod
    def from_result(cls, r: RollResult) -> "RollResponse":
        return cls(
            expression=r.expression, seed=r.seed, rolls=list(r.rolls), kept=list(r.kept),
            dropped=list(r.dropped), modifier=r.modifier, total=r.total,
        )


class ParseResponse(BaseModel):
    expression: str
    count: int
    sides: int
    modifier: int
    keep: list | None
    min_total: int
    max_total: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/parse", response_model=ParseResponse)
def parse_expression(expr: str = Query(..., description="Dice notation, e.g. 4d6kh3+1")) -> ParseResponse:
    try:
        d = parse(expr)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return ParseResponse(
        expression=str(d), count=d.count, sides=d.sides, modifier=d.modifier,
        keep=list(d.keep) if d.keep else None, min_total=d.min_total, max_total=d.max_total,
    )


@app.get("/roll", response_model=RollResponse)
def roll_dice(
    expr: str = Query(..., description="Dice notation, e.g. 3d6+2"),
    seed: int | None = Query(None, ge=0, description="Replay a previous roll exactly"),
) -> RollResponse:
    try:
        result = roll(expr, seed=seed)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return RollResponse.from_result(result)


@app.get("/limits")
def limits() -> dict[str, int]:
    return {"max_count": MAX_COUNT, "max_sides": MAX_SIDES}

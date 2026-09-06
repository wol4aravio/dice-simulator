"""Public request and response models for the dice API."""

from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr


class HealthResponse(BaseModel):
    """Service readiness response."""

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"status": "ok"}]}
    )

    status: str


class RollRequest(BaseModel):
    """Payload accepted by the roll endpoint."""

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"expression": "2d10 + 3", "seed": 42}]}
    )

    expression: StrictStr
    seed: StrictInt | None = None


class RollGroup(BaseModel):
    """The values produced for one dice group."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"count": 2, "sides": 10, "values": [4, 9], "subtotal": 13}]
        }
    )

    count: int
    sides: int
    values: list[int]
    subtotal: int


class RollResponse(BaseModel):
    """A successful, reproducible dice roll."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "expression": "2d10+3",
                    "seed": 42,
                    "rng_version": "v1",
                    "group": {
                        "count": 2,
                        "sides": 10,
                        "values": [4, 9],
                        "subtotal": 13,
                    },
                    "modifier": 3,
                    "total": 16,
                }
            ]
        }
    )

    expression: str
    seed: int
    rng_version: str
    group: RollGroup
    modifier: int
    total: int


class ErrorEnvelope(BaseModel):
    """Stable error representation returned by the public API."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "type": "https://dice-simulator.invalid/problems/expression-limit-exceeded",
                    "title": "Expression limit exceeded",
                    "status": 422,
                    "detail": "Dice count exceeds the maximum.",
                    "code": "expression_limit_exceeded",
                    "limit": 1000,
                    "actual": 1001,
                }
            ]
        }
    )

    type: str
    title: str
    status: int
    detail: str
    code: str
    limit: int | None = None
    actual: int | None = None

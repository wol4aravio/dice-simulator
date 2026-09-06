"""Public request and response models for the dice API."""

from pydantic import BaseModel, StrictInt, StrictStr


class RollRequest(BaseModel):
    """Payload accepted by the roll endpoint."""

    expression: StrictStr
    seed: StrictInt | None = None


class RollGroup(BaseModel):
    """The values produced for one dice group."""

    count: int
    sides: int
    values: list[int]
    subtotal: int


class RollResponse(BaseModel):
    """A successful, reproducible dice roll."""

    expression: str
    seed: int
    rng_version: str
    group: RollGroup
    modifier: int
    total: int


class ErrorEnvelope(BaseModel):
    """Stable error representation returned by the public API."""

    type: str
    title: str
    status: int
    detail: str
    code: str
    limit: int | None = None
    actual: int | None = None

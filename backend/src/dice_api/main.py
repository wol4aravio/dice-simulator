"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from dice_api.models import RollRequest, RollResponse
from dice_api.roller import roll
from dice_api.validation import PublicRollError, validate_roll_request

app = FastAPI(title="Dice Simulator API", version="0.1.0")


@app.exception_handler(PublicRollError)
def public_roll_error_handler(_request, error: PublicRollError) -> JSONResponse:
    """Return public domain-validation errors as the API error envelope."""
    return JSONResponse(
        status_code=error.status_code,
        content=error.to_envelope().model_dump(mode="json", exclude_none=True),
    )


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the API is ready to accept roll requests."""
    return {"status": "ok"}


@app.post("/roll", response_model=RollResponse)
def roll_dice(request: RollRequest) -> RollResponse:
    """Validate and execute a dice roll request."""
    return roll(validate_roll_request(request.expression, request.seed))

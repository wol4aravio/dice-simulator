"""FastAPI application entry point."""

from collections.abc import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from dice_api.models import RollRequest, RollResponse
from dice_api.roller import roll
from dice_api.validation import PublicRollError, validate_roll_request

app = FastAPI(title="Dice Simulator API", version="0.1.0")


@app.middleware("http")
async def require_json_roll_requests(
    request: Request, call_next: Callable[[Request], Response]
) -> Response:
    """Reject non-JSON roll requests before request-body parsing."""
    if request.url.path == "/roll" and request.method == "POST":
        media_type = request.headers.get("content-type", "").split(";", 1)[0].lower()
        if media_type != "application/json":
            return _public_error_response(
                PublicRollError(
                    status_code=415,
                    code="unsupported_media_type",
                    title="Unsupported media type",
                    detail="POST /roll requires application/json.",
                )
            )

    return await call_next(request)


@app.exception_handler(PublicRollError)
def public_roll_error_handler(_request: Request, error: PublicRollError) -> JSONResponse:
    """Return public domain-validation errors as the API error envelope."""
    return _public_error_response(error)


@app.exception_handler(RequestValidationError)
def request_validation_error_handler(
    _request: Request, error: RequestValidationError
) -> JSONResponse:
    """Map framework request failures to the stable public error envelope."""
    errors = error.errors()
    if any(item.get("type") == "json_invalid" for item in errors):
        return _public_error_response(
            PublicRollError(
                status_code=400,
                code="invalid_json",
                title="Invalid JSON",
                detail="Request body must contain valid JSON.",
            )
        )

    field_names = {str(part) for item in errors for part in item.get("loc", ())}
    if "seed" in field_names:
        return _public_error_response(
            PublicRollError(
                status_code=422,
                code="invalid_seed",
                title="Invalid seed",
                detail="Seed must be an integer.",
            )
        )

    return _public_error_response(
        PublicRollError(
            status_code=422,
            code="invalid_expression",
            title="Invalid expression",
            detail="Expression must be a string.",
        )
    )


def _public_error_response(error: PublicRollError) -> JSONResponse:
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

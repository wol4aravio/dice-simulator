"""FastAPI application entry point."""

from collections.abc import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from dice_api.models import ErrorEnvelope, HealthResponse, RollRequest, RollResponse
from dice_api.roller import roll
from dice_api.validation import PublicRollError, validate_roll_request

ROLL_ERROR_RESPONSES = {
    400: {
        "model": ErrorEnvelope,
        "description": "Invalid JSON request body.",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_json": {
                        "summary": "Invalid JSON",
                        "value": {
                            "type": "https://dice-simulator.invalid/problems/invalid-json",
                            "title": "Invalid JSON",
                            "status": 400,
                            "detail": "Request body must contain valid JSON.",
                            "code": "invalid_json",
                        },
                    }
                }
            }
        },
    },
    415: {
        "model": ErrorEnvelope,
        "description": "Unsupported request media type.",
        "content": {
            "application/json": {
                "examples": {
                    "unsupported_media_type": {
                        "summary": "Unsupported media type",
                        "value": {
                            "type": "https://dice-simulator.invalid/problems/unsupported-media-type",
                            "title": "Unsupported media type",
                            "status": 415,
                            "detail": "POST /roll requires application/json.",
                            "code": "unsupported_media_type",
                        },
                    }
                }
            }
        },
    },
    422: {
        "model": ErrorEnvelope,
        "description": "Invalid seed, expression, request field, or resource limit.",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_seed": {
                        "summary": "Invalid seed",
                        "value": {
                            "type": "https://dice-simulator.invalid/problems/invalid-seed",
                            "title": "Invalid seed",
                            "status": 422,
                            "detail": "Seed must be an integer.",
                            "code": "invalid_seed",
                        },
                    },
                    "invalid_expression": {
                        "summary": "Invalid expression",
                        "value": {
                            "type": "https://dice-simulator.invalid/problems/invalid-expression",
                            "title": "Invalid expression",
                            "status": 422,
                            "detail": "Unsupported dice expression.",
                            "code": "invalid_expression",
                        },
                    },
                    "expression_limit_exceeded": {
                        "summary": "Expression limit exceeded",
                        "value": {
                            "type": "https://dice-simulator.invalid/problems/expression-limit-exceeded",
                            "title": "Expression limit exceeded",
                            "status": 422,
                            "detail": "Dice count exceeds the maximum.",
                            "code": "expression_limit_exceeded",
                            "limit": 1000,
                            "actual": 1001,
                        },
                    },
                }
            }
        },
    },
}

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


@app.get(
    "/health",
    response_model=HealthResponse,
    responses={
        200: {
            "description": "The API is ready to accept roll requests.",
            "content": {
                "application/json": {
                    "example": {"status": "ok"},
                }
            },
        }
    },
)
def health() -> HealthResponse:
    """Report that the API is ready to accept roll requests."""
    return HealthResponse(status="ok")


@app.post("/roll", response_model=RollResponse, responses=ROLL_ERROR_RESPONSES)
def roll_dice(request: RollRequest) -> RollResponse:
    """Validate and execute a dice roll request."""
    return roll(validate_roll_request(request.expression, request.seed))

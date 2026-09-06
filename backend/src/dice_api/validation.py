"""Pre-execution validation for roll requests and resource limits."""

from dataclasses import dataclass
from typing import Final

from dice_api.models import ErrorEnvelope
from dice_api.parser import InvalidRollExpression, ParsedRollExpression, parse_roll_expression

MAX_EXPRESSION_LENGTH: Final = 256
MAX_DICE_COUNT: Final = 1_000
MIN_DICE_SIDES: Final = 2
MAX_DICE_SIDES: Final = 1_000_000
MAX_ABS_MODIFIER: Final = 1_000_000_000
MAX_ABS_SEED: Final = (2**63) - 1

_PROBLEM_BASE: Final = "https://dice-simulator.invalid/problems"


@dataclass(frozen=True, slots=True)
class PublicRollError(ValueError):
    """A client-visible validation failure with stable public metadata."""

    status_code: int
    code: str
    title: str
    detail: str
    limit: int | None = None
    actual: int | None = None

    def to_envelope(self) -> ErrorEnvelope:
        """Return the public error response body for this validation failure."""
        return ErrorEnvelope(
            type=f"{_PROBLEM_BASE}/{self.code.replace('_', '-')}",
            title=self.title,
            status=self.status_code,
            detail=self.detail,
            code=self.code,
            limit=self.limit,
            actual=self.actual,
        )


@dataclass(frozen=True, slots=True)
class ValidatedRollRequest:
    """A parsed request that is safe to execute."""

    expression: ParsedRollExpression
    seed: int | None


def validate_roll_request(expression: str, seed: int | None = None) -> ValidatedRollRequest:
    """Parse and validate a roll request before constructing RNG state or values."""
    _validate_expression_length(expression)
    parsed = _parse_expression(expression)
    _validate_roll_limits(parsed)
    _validate_seed(seed)
    return ValidatedRollRequest(expression=parsed, seed=seed)


def _validate_expression_length(expression: str) -> None:
    if not isinstance(expression, str):
        raise _invalid_expression("Expression must be a string.")

    actual = len(expression)
    if actual > MAX_EXPRESSION_LENGTH:
        raise _expression_limit_exceeded(
            "Expression length exceeds the maximum.",
            limit=MAX_EXPRESSION_LENGTH,
            actual=actual,
        )


def _parse_expression(expression: str) -> ParsedRollExpression:
    try:
        return parse_roll_expression(expression)
    except InvalidRollExpression as error:
        raise _invalid_expression("Unsupported dice expression.") from error


def _validate_roll_limits(parsed: ParsedRollExpression) -> None:
    if parsed.sides < MIN_DICE_SIDES:
        raise _invalid_expression("Dice sides must be at least 2.")

    if parsed.count > MAX_DICE_COUNT:
        raise _expression_limit_exceeded(
            "Dice count exceeds the maximum.",
            limit=MAX_DICE_COUNT,
            actual=parsed.count,
        )

    if parsed.sides > MAX_DICE_SIDES:
        raise _expression_limit_exceeded(
            "Dice sides exceed the maximum.",
            limit=MAX_DICE_SIDES,
            actual=parsed.sides,
        )

    actual_modifier = abs(parsed.modifier)
    if actual_modifier > MAX_ABS_MODIFIER:
        raise _expression_limit_exceeded(
            "Modifier magnitude exceeds the maximum.",
            limit=MAX_ABS_MODIFIER,
            actual=actual_modifier,
        )


def _validate_seed(seed: int | None) -> None:
    if seed is None:
        return

    if not isinstance(seed, int) or isinstance(seed, bool):
        raise _invalid_seed("Seed must be an integer.")

    if abs(seed) > MAX_ABS_SEED:
        raise _invalid_seed("Seed magnitude exceeds the maximum.")


def _invalid_expression(detail: str) -> PublicRollError:
    return PublicRollError(
        status_code=422,
        code="invalid_expression",
        title="Invalid expression",
        detail=detail,
    )


def _invalid_seed(detail: str) -> PublicRollError:
    return PublicRollError(
        status_code=422,
        code="invalid_seed",
        title="Invalid seed",
        detail=detail,
    )


def _expression_limit_exceeded(detail: str, *, limit: int, actual: int) -> PublicRollError:
    return PublicRollError(
        status_code=422,
        code="expression_limit_exceeded",
        title="Expression limit exceeded",
        detail=detail,
        limit=limit,
        actual=actual,
    )

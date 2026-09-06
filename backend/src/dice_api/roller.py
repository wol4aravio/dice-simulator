"""Versioned deterministic dice rolling."""

from hashlib import sha256
import secrets
from typing import Final

from dice_api.models import RollGroup, RollResponse
from dice_api.parser import ParsedRollExpression
from dice_api.validation import MAX_ABS_SEED, ValidatedRollRequest

RNG_VERSION: Final = "v1"
_SEED_BYTES: Final = 8


def roll(validated: ValidatedRollRequest) -> RollResponse:
    """Execute a validated roll request and return a replayable response."""
    expression = validated.expression
    seed = validated.seed if validated.seed is not None else generate_seed()
    values = _roll_values(expression, seed)
    subtotal = sum(values)
    total = subtotal + expression.modifier

    return RollResponse(
        expression=expression.normalized,
        seed=seed,
        rng_version=RNG_VERSION,
        group=RollGroup(
            count=expression.count,
            sides=expression.sides,
            values=values,
            subtotal=subtotal,
        ),
        modifier=expression.modifier,
        total=total,
    )


def generate_seed() -> int:
    """Generate a replay seed using operating-system entropy."""
    return secrets.randbelow(MAX_ABS_SEED + 1)


def _roll_values(expression: ParsedRollExpression, seed: int) -> list[int]:
    return [_roll_one(expression.normalized, seed, expression.sides, index) for index in range(expression.count)]


def _roll_one(normalized_expression: str, seed: int, sides: int, index: int) -> int:
    digest = sha256(
        b"|".join(
            (
                b"dice-simulator-api",
                RNG_VERSION.encode("ascii"),
                str(seed).encode("ascii"),
                normalized_expression.encode("ascii"),
                index.to_bytes(_SEED_BYTES, "big", signed=False),
            )
        )
    ).digest()
    return (int.from_bytes(digest, "big") % sides) + 1

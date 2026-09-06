"""Parsing for the initial, single-group dice expression language."""

from dataclasses import dataclass
import re


_ASCII_WHITESPACE = re.compile(r"[ \t\n\r\f\v]+")
_EXPRESSION = re.compile(
    r"(?P<count>[0-9]+)d(?P<sides>[0-9]+)(?P<modifier>[+-][0-9]+)?"
)


class InvalidRollExpression(ValueError):
    """Raised when input is outside the supported dice-expression grammar."""


@dataclass(frozen=True, slots=True)
class ParsedRollExpression:
    """A normalized, parsed single dice group and its optional modifier."""

    count: int
    sides: int
    modifier: int

    @property
    def normalized(self) -> str:
        """Return the canonical expression without whitespace or leading zeroes."""
        expression = f"{self.count}d{self.sides}"
        return f"{expression}{self.modifier:+d}" if self.modifier else expression


def parse_roll_expression(expression: str) -> ParsedRollExpression:
    """Parse one positive ``NdM`` group and an optional signed modifier.

    Only ASCII whitespace is removed. All other whitespace and unsupported dice
    notation are rejected instead of being silently normalized.
    """
    if not isinstance(expression, str):
        raise InvalidRollExpression("Expression must be a string.")

    compact_expression = _ASCII_WHITESPACE.sub("", expression)
    match = _EXPRESSION.fullmatch(compact_expression)
    if match is None:
        raise InvalidRollExpression("Unsupported dice expression.")

    try:
        count = int(match["count"])
        sides = int(match["sides"])
        modifier = int(match["modifier"] or "0")
    except ValueError as error:
        raise InvalidRollExpression("Unsupported dice expression.") from error

    if count < 1 or sides < 1:
        raise InvalidRollExpression("Dice count and sides must be positive.")

    return ParsedRollExpression(count=count, sides=sides, modifier=modifier)

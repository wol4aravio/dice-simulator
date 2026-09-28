"""Dice notation parser.

Grammar (case-insensitive, whitespace ignored):

    expr     := [count] 'd' sides [keep] [modifier]
    count    := integer >= 1          (default 1)
    sides    := integer >= 2
    keep     := ('kh' | 'kl') integer (1 <= n <= count)
    modifier := ('+' | '-') integer

Examples: "d20", "3d6", "3d6+2", "4d6kh3", "2d20kl1-1".
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

MAX_COUNT = 1000
MAX_SIDES = 10_000

_PATTERN = re.compile(
    r"""^
    (?P<count>\d+)?
    d
    (?P<sides>\d+)
    (?:k(?P<keep_mode>[hl])(?P<keep_n>\d+))?
    (?:(?P<mod_sign>[+-])(?P<mod>\d+))?
    $""",
    re.VERBOSE,
)

KeepMode = Literal["high", "low"]


@dataclass(frozen=True, slots=True)
class DiceExpr:
    count: int
    sides: int
    modifier: int = 0
    keep: tuple[KeepMode, int] | None = None

    def __str__(self) -> str:
        s = f"{self.count}d{self.sides}"
        if self.keep:
            s += f"k{'h' if self.keep[0] == 'high' else 'l'}{self.keep[1]}"
        if self.modifier:
            s += f"{self.modifier:+d}"
        return s

    @property
    def kept(self) -> int:
        """How many dice contribute to the sum."""
        return self.keep[1] if self.keep else self.count

    @property
    def min_total(self) -> int:
        return self.kept + self.modifier

    @property
    def max_total(self) -> int:
        return self.kept * self.sides + self.modifier


def parse(expr: str) -> DiceExpr:
    """Parse dice notation into a DiceExpr. Raises ValueError with an actionable message."""
    if not isinstance(expr, str):
        raise ValueError("dice expression must be a string like '3d6+2'")
    text = re.sub(r"\s+", "", expr).lower()
    if not text:
        raise ValueError("empty dice expression; expected something like '3d6+2'")
    m = _PATTERN.match(text)
    if not m:
        raise ValueError(f"invalid dice expression {expr!r}; expected [N]dM[khX|klX][+K|-K], e.g. '4d6kh3+1'")

    count = int(m.group("count")) if m.group("count") else 1
    sides = int(m.group("sides"))
    if count < 1:
        raise ValueError("dice count must be at least 1")
    if count > MAX_COUNT:
        raise ValueError(f"dice count must be at most {MAX_COUNT}")
    if sides < 2:
        raise ValueError("a die must have at least 2 sides")
    if sides > MAX_SIDES:
        raise ValueError(f"a die may have at most {MAX_SIDES} sides")

    keep: tuple[KeepMode, int] | None = None
    if m.group("keep_mode"):
        n = int(m.group("keep_n"))
        if n < 1 or n > count:
            raise ValueError(f"keep count must be between 1 and {count} (got {n})")
        keep = ("high" if m.group("keep_mode") == "h" else "low", n)

    modifier = 0
    if m.group("mod"):
        modifier = int(m.group("mod"))
        if m.group("mod_sign") == "-":
            modifier = -modifier

    return DiceExpr(count=count, sides=sides, modifier=modifier, keep=keep)

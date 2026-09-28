"""Pure domain layer: no HTTP, no I/O. Everything here is testable without FastAPI."""
from .parser import MAX_COUNT, MAX_SIDES, DiceExpr, parse
from .roller import RollResult, new_seed, roll
from .stats import DiceStats, stats

__all__ = [
    "MAX_COUNT",
    "MAX_SIDES",
    "DiceExpr",
    "parse",
    "RollResult",
    "new_seed",
    "roll",
    "DiceStats",
    "stats",
]

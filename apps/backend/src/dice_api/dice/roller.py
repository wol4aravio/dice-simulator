"""Rolling: deterministic given a seed, otherwise random.

Reproducibility rule for the whole project: every random result carries the
seed that produced it, so any roll can be replayed exactly.
"""
from __future__ import annotations

import random
import secrets
from dataclasses import dataclass, field

from .parser import DiceExpr, parse


@dataclass(frozen=True, slots=True)
class RollResult:
    expression: str
    seed: int
    rolls: tuple[int, ...]          # every die as rolled, in order
    kept: tuple[int, ...]           # dice that count towards the total
    modifier: int
    total: int
    dropped: tuple[int, ...] = field(default_factory=tuple)


def new_seed() -> int:
    """A fresh 63-bit seed; large enough to never collide in practice, small enough for JSON."""
    return secrets.randbits(63)


def roll(expr: DiceExpr | str, seed: int | None = None) -> RollResult:
    dice = parse(expr) if isinstance(expr, str) else expr
    if seed is None:
        seed = new_seed()
    rng = random.Random(seed)
    rolls = tuple(rng.randint(1, dice.sides) for _ in range(dice.count))

    if dice.keep is None:
        kept, dropped = rolls, ()
    else:
        mode, n = dice.keep
        order = sorted(range(dice.count), key=lambda i: rolls[i], reverse=(mode == "high"))
        keep_idx = set(order[:n])
        kept = tuple(v for i, v in enumerate(rolls) if i in keep_idx)
        dropped = tuple(v for i, v in enumerate(rolls) if i not in keep_idx)

    return RollResult(
        expression=str(dice),
        seed=seed,
        rolls=rolls,
        kept=kept,
        modifier=dice.modifier,
        total=sum(kept) + dice.modifier,
        dropped=dropped,
    )

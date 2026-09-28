"""Deterministic statistics for dice expressions."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .parser import DiceExpr, parse


@dataclass(frozen=True, slots=True)
class DiceStats:
    """The attainable bounds and expected total for a dice expression."""

    expression: str
    minimum: int
    maximum: int
    mean: float


def stats(expr: DiceExpr | str) -> DiceStats:
    """Return deterministic bounds and the mathematical expected total for an expression."""
    dice = parse(expr) if isinstance(expr, str) else expr
    mean = _expected_kept_sum(dice) + dice.modifier
    return DiceStats(
        expression=str(dice),
        minimum=dice.min_total,
        maximum=dice.max_total,
        mean=mean,
    )


def _expected_kept_sum(dice: DiceExpr) -> float:
    if dice.keep is None:
        return dice.count * (dice.sides + 1) / 2

    mode, kept = dice.keep
    highest_sum = _expected_highest_sum(dice.count, dice.sides, kept)
    if mode == "high":
        return highest_sum
    return kept * (dice.sides + 1) - highest_sum


def _expected_highest_sum(count: int, sides: int, kept: int) -> float:
    """Return the expected sum of the highest kept dice using binomial tail probabilities."""
    return sum(_expected_capped_binomial(count, face / sides, kept) for face in range(1, sides + 1))


def _expected_capped_binomial(count: int, probability: float, cap: int) -> float:
    """Return E[min(cap, X)] for X distributed as Binomial(count, probability)."""
    if probability == 0:
        return 0.0
    if probability == 1:
        return float(cap)

    if cap <= count / 2:
        deficit = 0.0
        outcome = cap - 1
        mass = _binomial_mass(count, outcome, probability)
        while outcome >= 0:
            deficit += (cap - outcome) * mass
            if outcome == 0:
                break
            mass *= outcome / (count - outcome + 1) * (1 - probability) / probability
            outcome -= 1
        return cap - deficit

    excess = 0.0
    outcome = cap + 1
    mass = _binomial_mass(count, outcome, probability)
    while outcome <= count:
        excess += (outcome - cap) * mass
        if outcome == count:
            break
        mass *= (count - outcome) / (outcome + 1) * probability / (1 - probability)
        outcome += 1
    return count * probability - excess


def _binomial_mass(count: int, outcome: int, probability: float) -> float:
    """Return the probability mass for one binomial outcome without overflowing intermediates."""
    log_mass = (
        math.lgamma(count + 1)
        - math.lgamma(outcome + 1)
        - math.lgamma(count - outcome + 1)
        + outcome * math.log(probability)
        + (count - outcome) * math.log1p(-probability)
    )
    return math.exp(log_mass)

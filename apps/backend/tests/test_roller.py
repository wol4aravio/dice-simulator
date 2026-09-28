import pytest

from dice_api.dice import parse, roll


def test_seed_makes_rolls_reproducible():
    a = roll("10d20", seed=42)
    b = roll("10d20", seed=42)
    assert a == b
    assert roll("10d20", seed=43) != a


def test_rolls_are_within_bounds():
    for seed in range(50):
        r = roll("6d6+3", seed=seed)
        assert all(1 <= v <= 6 for v in r.rolls)
        assert r.total == sum(r.rolls) + 3
        assert 9 <= r.total <= 39


def test_keep_highest_and_lowest():
    r = roll("4d6kh3", seed=7)
    assert len(r.kept) == 3 and len(r.dropped) == 1
    assert min(r.kept) >= max(r.dropped)
    assert sorted(r.kept + r.dropped) == sorted(r.rolls)
    assert r.total == sum(r.kept)

    r = roll("2d20kl1", seed=7)
    assert len(r.kept) == 1 and r.kept[0] == min(r.rolls)


def test_fresh_seed_when_none_given():
    r1, r2 = roll("d20"), roll("d20")
    assert r1.seed != r2.seed
    assert roll("d20", seed=r1.seed) == r1  # replay from the returned seed


def test_accepts_parsed_expression():
    d = parse("3d6")
    assert roll(d, seed=1).expression == "3d6"


def test_invalid_expression_propagates():
    with pytest.raises(ValueError):
        roll("abc")

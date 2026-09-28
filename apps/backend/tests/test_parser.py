import pytest

from dice_api.dice import DiceExpr, parse


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("d20", DiceExpr(1, 20)),
        ("3d6", DiceExpr(3, 6)),
        ("3d6+2", DiceExpr(3, 6, 2)),
        ("3d6-1", DiceExpr(3, 6, -1)),
        ("4d6kh3", DiceExpr(4, 6, 0, ("high", 3))),
        ("2d20kl1", DiceExpr(2, 20, 0, ("low", 1))),
        ("4D6KH3+1", DiceExpr(4, 6, 1, ("high", 3))),
        (" 2 d 8 + 3 ", DiceExpr(2, 8, 3)),
    ],
)
def test_valid_expressions(expr, expected):
    assert parse(expr) == expected


@pytest.mark.parametrize(
    "expr, fragment",
    [
        ("0d6", "at least 1"),
        ("3d0", "at least 2"),
        ("3d1", "at least 2"),
        ("abc", "invalid dice expression"),
        ("4d6kh5", "between 1 and 4"),
        ("4d6kh0", "between 1 and 4"),
        ("", "empty"),
        ("1001d6", "at most 1000"),
        ("d10001", "at most 10000"),
        ("3d6+", "invalid dice expression"),
    ],
)
def test_invalid_expressions(expr, fragment):
    with pytest.raises(ValueError) as e:
        parse(expr)
    assert fragment in str(e.value)


def test_str_roundtrip_and_bounds():
    d = parse("4d6kh3+1")
    assert str(d) == "4d6kh3+1"
    assert (d.min_total, d.max_total) == (4, 19)
    assert parse("2d20kl1-1").min_total == 0
    assert parse(str(parse("3d6-2"))) == parse("3d6-2")

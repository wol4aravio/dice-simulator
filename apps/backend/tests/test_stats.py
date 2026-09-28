import pytest

from dice_api.dice import stats


@pytest.mark.parametrize(
    ("expr", "expression", "minimum", "maximum", "mean"),
    [
        ("d6", "1d6", 1, 6, 3.5),
        ("3d6+2", "3d6+2", 5, 20, 12.5),
        ("2d6kh1", "2d6kh1", 1, 6, 161 / 36),
        ("2d6kl1-1", "2d6kl1-1", 0, 5, 55 / 36),
        ("4d6kh3+1", "4d6kh3+1", 4, 19, 1 + 15869 / 1296),
    ],
)
def test_stats_for_dice_expression(expr, expression, minimum, maximum, mean):
    result = stats(expr)

    assert result.expression == expression
    assert result.minimum == minimum
    assert result.maximum == maximum
    assert result.mean == pytest.approx(mean)


def test_stats_propagates_invalid_expression():
    with pytest.raises(ValueError) as e:
        stats("4d6kh5")

    assert "between 1 and 4" in str(e.value)

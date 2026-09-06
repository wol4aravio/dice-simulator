"""Table-driven tests for dice-expression parsing and normalization."""

import unittest

from dice_api.parser import InvalidRollExpression, parse_roll_expression


class DiceExpressionParserTests(unittest.TestCase):
    def test_parses_and_normalizes_supported_expressions(self) -> None:
        cases = (
            ("1d20", 1, 20, 0, "1d20"),
            ("2d10 + 3", 2, 10, 3, "2d10+3"),
            (" 3 d 8 - 2\t", 3, 8, -2, "3d8-2"),
            ("\t001d006 + 0003\r\n", 1, 6, 3, "1d6+3"),
            ("1d6+0", 1, 6, 0, "1d6"),
        )

        for expression, count, sides, modifier, normalized in cases:
            with self.subTest(expression=expression):
                parsed = parse_roll_expression(expression)

                self.assertEqual(parsed.count, count)
                self.assertEqual(parsed.sides, sides)
                self.assertEqual(parsed.modifier, modifier)
                self.assertEqual(parsed.normalized, normalized)

    def test_rejects_unsupported_or_invalid_expressions(self) -> None:
        cases = (
            "d20",
            "2d",
            "0d6",
            "1d0",
            "2D6",
            "1d6+",
            "1d6-2+1",
            "1d6/2",
            "2d6+1d4",
            "(1d6)",
            "1d6kh1",
            "1d6\u00a0+1",
        )

        for expression in cases:
            with self.subTest(expression=expression):
                with self.assertRaises(InvalidRollExpression):
                    parse_roll_expression(expression)

    def test_rejects_non_string_expression(self) -> None:
        with self.assertRaises(InvalidRollExpression):
            parse_roll_expression(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

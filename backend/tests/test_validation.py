"""Tests for pre-execution roll validation and public error metadata."""

import unittest

from dice_api.validation import (
    MAX_ABS_MODIFIER,
    MAX_ABS_SEED,
    MAX_DICE_COUNT,
    MAX_DICE_SIDES,
    MAX_EXPRESSION_LENGTH,
    PublicRollError,
    validate_roll_request,
)


class RollValidationTests(unittest.TestCase):
    def test_accepts_expression_at_resource_limits_and_seed_bounds(self) -> None:
        validated = validate_roll_request(
            f"{MAX_DICE_COUNT}d{MAX_DICE_SIDES}+{MAX_ABS_MODIFIER}",
            seed=-MAX_ABS_SEED,
        )

        self.assertEqual(validated.expression.count, MAX_DICE_COUNT)
        self.assertEqual(validated.expression.sides, MAX_DICE_SIDES)
        self.assertEqual(validated.expression.modifier, MAX_ABS_MODIFIER)
        self.assertEqual(validated.seed, -MAX_ABS_SEED)

    def test_expression_length_limit_maps_to_http_422_limit_error(self) -> None:
        expression = f"1d6+{'1' * MAX_EXPRESSION_LENGTH}"

        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request(expression)

        self.assert_public_error(
            raised.exception,
            code="expression_limit_exceeded",
            limit=MAX_EXPRESSION_LENGTH,
            actual=len(expression),
        )

    def test_dice_count_limit_maps_to_http_422_limit_error(self) -> None:
        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request(f"{MAX_DICE_COUNT + 1}d6")

        self.assert_public_error(
            raised.exception,
            code="expression_limit_exceeded",
            limit=MAX_DICE_COUNT,
            actual=MAX_DICE_COUNT + 1,
        )

    def test_sides_upper_limit_maps_to_http_422_limit_error(self) -> None:
        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request(f"1d{MAX_DICE_SIDES + 1}")

        self.assert_public_error(
            raised.exception,
            code="expression_limit_exceeded",
            limit=MAX_DICE_SIDES,
            actual=MAX_DICE_SIDES + 1,
        )

    def test_sides_below_two_maps_to_invalid_expression(self) -> None:
        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request("1d1")

        self.assert_public_error(raised.exception, code="invalid_expression")

    def test_modifier_limit_maps_to_http_422_limit_error(self) -> None:
        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request(f"1d6-{MAX_ABS_MODIFIER + 1}")

        self.assert_public_error(
            raised.exception,
            code="expression_limit_exceeded",
            limit=MAX_ABS_MODIFIER,
            actual=MAX_ABS_MODIFIER + 1,
        )

    def test_seed_bound_maps_to_invalid_seed(self) -> None:
        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request("1d6", seed=MAX_ABS_SEED + 1)

        self.assert_public_error(raised.exception, code="invalid_seed")

    def test_non_integer_seed_maps_to_invalid_seed(self) -> None:
        with self.assertRaises(PublicRollError) as raised:
            validate_roll_request("1d6", seed=True)  # type: ignore[arg-type]

        self.assert_public_error(raised.exception, code="invalid_seed")

    def assert_public_error(
        self,
        error: PublicRollError,
        *,
        code: str,
        limit: int | None = None,
        actual: int | None = None,
    ) -> None:
        self.assertEqual(error.status_code, 422)
        self.assertEqual(error.code, code)
        envelope = error.to_envelope().model_dump(mode="json", exclude_none=True)
        self.assertEqual(envelope["status"], 422)
        self.assertEqual(envelope["code"], code)
        if limit is not None:
            self.assertEqual(envelope["limit"], limit)
            self.assertEqual(envelope["actual"], actual)
        else:
            self.assertNotIn("limit", envelope)
            self.assertNotIn("actual", envelope)


if __name__ == "__main__":
    unittest.main()

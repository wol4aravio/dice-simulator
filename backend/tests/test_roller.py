"""Tests for versioned deterministic dice rolling."""

import unittest

from dice_api.roller import RNG_VERSION, roll
from dice_api.validation import MAX_ABS_SEED, validate_roll_request


class DiceRollerTests(unittest.TestCase):
    def test_seeded_roll_replays_values_subtotal_and_total(self) -> None:
        request = validate_roll_request("2d10 + 3", seed=42)

        first = roll(request)
        second = roll(request)

        self.assertEqual(first.rng_version, RNG_VERSION)
        self.assertEqual(first.model_dump(mode="json"), second.model_dump(mode="json"))
        self.assertEqual(first.expression, "2d10+3")
        self.assertEqual(first.seed, 42)
        self.assertEqual(first.group.count, 2)
        self.assertEqual(first.group.sides, 10)
        self.assertEqual(len(first.group.values), 2)
        self.assertTrue(all(1 <= value <= 10 for value in first.group.values))
        self.assertEqual(first.group.subtotal, sum(first.group.values))
        self.assertEqual(first.modifier, 3)
        self.assertEqual(first.total, first.group.subtotal + first.modifier)

    def test_same_seed_with_different_normalized_expression_changes_stream(self) -> None:
        d6_response = roll(validate_roll_request("2d6", seed=42))
        d10_response = roll(validate_roll_request("2d10", seed=42))

        self.assertNotEqual(d6_response.group.values, d10_response.group.values)

    def test_unseeded_roll_returns_replayable_entropy_seed(self) -> None:
        unseeded = roll(validate_roll_request("3d8-2"))
        replayed = roll(validate_roll_request(unseeded.expression, seed=unseeded.seed))

        self.assertIsInstance(unseeded.seed, int)
        self.assertGreaterEqual(unseeded.seed, 0)
        self.assertLessEqual(unseeded.seed, MAX_ABS_SEED)
        self.assertEqual(unseeded.rng_version, RNG_VERSION)
        self.assertEqual(unseeded.model_dump(mode="json"), replayed.model_dump(mode="json"))


if __name__ == "__main__":
    unittest.main()

"""Serialization tests for the public dice API models."""

import unittest

from dice_api.models import ErrorEnvelope, RollGroup, RollRequest, RollResponse


class RollModelSerializationTests(unittest.TestCase):
    def test_request_serializes_expression_and_optional_seed(self) -> None:
        request = RollRequest(expression="2d10 + 3", seed=42)

        self.assertEqual(
            request.model_dump(mode="json", exclude_none=True),
            {"expression": "2d10 + 3", "seed": 42},
        )

    def test_request_omits_absent_seed(self) -> None:
        request = RollRequest(expression="1d6")

        self.assertEqual(
            request.model_dump(mode="json", exclude_none=True),
            {"expression": "1d6"},
        )

    def test_success_response_serializes_roll_group_and_total(self) -> None:
        response = RollResponse(
            expression="2d10+3",
            seed=42,
            rng_version="v1",
            group=RollGroup(count=2, sides=10, values=[4, 9], subtotal=13),
            modifier=3,
            total=16,
        )

        self.assertEqual(
            response.model_dump(mode="json"),
            {
                "expression": "2d10+3",
                "seed": 42,
                "rng_version": "v1",
                "group": {
                    "count": 2,
                    "sides": 10,
                    "values": [4, 9],
                    "subtotal": 13,
                },
                "modifier": 3,
                "total": 16,
            },
        )

    def test_error_envelope_serializes_required_and_limit_fields(self) -> None:
        error = ErrorEnvelope(
            type="https://example.invalid/problems/expression-limit-exceeded",
            title="Expression limit exceeded",
            status=422,
            detail="Dice count exceeds the maximum.",
            code="expression_limit_exceeded",
            limit=1000,
            actual=1001,
        )

        self.assertEqual(
            error.model_dump(mode="json", exclude_none=True),
            {
                "type": "https://example.invalid/problems/expression-limit-exceeded",
                "title": "Expression limit exceeded",
                "status": 422,
                "detail": "Dice count exceeds the maximum.",
                "code": "expression_limit_exceeded",
                "limit": 1000,
                "actual": 1001,
            },
        )


if __name__ == "__main__":
    unittest.main()

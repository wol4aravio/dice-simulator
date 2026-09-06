"""Tests that generated OpenAPI docs publish public contract examples."""

import unittest

from dice_api.main import app


class OpenApiExamplesTests(unittest.TestCase):
    def test_health_endpoint_publishes_response_example(self) -> None:
        operation = app.openapi()["paths"]["/health"]["get"]

        example = operation["responses"]["200"]["content"]["application/json"]["example"]
        self.assertEqual(example, {"status": "ok"})

    def test_roll_endpoint_publishes_request_and_success_examples(self) -> None:
        operation = app.openapi()["paths"]["/roll"]["post"]
        schemas = app.openapi()["components"]["schemas"]

        request_examples = schemas["RollRequest"]["examples"]
        success_examples = schemas["RollResponse"]["examples"]

        self.assertIn({"expression": "2d10 + 3", "seed": 42}, request_examples)
        self.assertEqual(success_examples[0]["expression"], "2d10+3")
        self.assertEqual(success_examples[0]["rng_version"], "v1")
        self.assertEqual(success_examples[0]["group"]["count"], 2)
        self.assertIn("200", operation["responses"])

    def test_roll_endpoint_publishes_error_examples(self) -> None:
        operation = app.openapi()["paths"]["/roll"]["post"]

        invalid_json = self.example(operation, "400", "invalid_json")
        unsupported_media_type = self.example(
            operation, "415", "unsupported_media_type"
        )
        invalid_seed = self.example(operation, "422", "invalid_seed")
        invalid_expression = self.example(operation, "422", "invalid_expression")
        limit_exceeded = self.example(operation, "422", "expression_limit_exceeded")

        self.assertEqual(invalid_json["code"], "invalid_json")
        self.assertEqual(unsupported_media_type["code"], "unsupported_media_type")
        self.assertEqual(invalid_seed["code"], "invalid_seed")
        self.assertEqual(invalid_expression["code"], "invalid_expression")
        self.assertEqual(limit_exceeded["code"], "expression_limit_exceeded")
        self.assertEqual(limit_exceeded["limit"], 1000)
        self.assertEqual(limit_exceeded["actual"], 1001)

    def example(self, operation: dict, status: str, name: str) -> dict:
        return operation["responses"][status]["content"]["application/json"]["examples"][
            name
        ]["value"]


if __name__ == "__main__":
    unittest.main()

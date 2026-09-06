"""Endpoint tests for successful dice rolls."""

import unittest

import httpx

from dice_api.main import app


class RollEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def test_roll_with_seed_returns_replayable_success_response(self) -> None:
        first = await self.post_roll({"expression": "2d10 + 3", "seed": 42})
        second = await self.post_roll({"expression": "2d10 + 3", "seed": 42})

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json(), second.json())

        body = first.json()
        self.assertEqual(body["expression"], "2d10+3")
        self.assertEqual(body["seed"], 42)
        self.assertEqual(body["rng_version"], "v1")
        self.assertEqual(body["group"]["count"], 2)
        self.assertEqual(body["group"]["sides"], 10)
        self.assertEqual(len(body["group"]["values"]), 2)
        self.assertTrue(all(1 <= value <= 10 for value in body["group"]["values"]))
        self.assertEqual(body["group"]["subtotal"], sum(body["group"]["values"]))
        self.assertEqual(body["modifier"], 3)
        self.assertEqual(body["total"], body["group"]["subtotal"] + 3)

    async def test_roll_without_seed_returns_seed_that_replays_response(self) -> None:
        unseeded = await self.post_roll({"expression": "3d8 - 2"})

        self.assertEqual(unseeded.status_code, 200)
        body = unseeded.json()
        self.assertIsInstance(body["seed"], int)
        self.assertEqual(body["expression"], "3d8-2")
        self.assertEqual(body["rng_version"], "v1")

        replayed = await self.post_roll(
            {"expression": body["expression"], "seed": body["seed"]}
        )

        self.assertEqual(replayed.status_code, 200)
        self.assertEqual(replayed.json(), body)

    async def test_invalid_json_returns_public_error_envelope(self) -> None:
        response = await self.post_roll_raw(
            content="{not-json", headers={"content-type": "application/json"}
        )

        self.assert_public_error(response, status_code=400, code="invalid_json")

    async def test_unsupported_media_type_returns_public_error_envelope(self) -> None:
        response = await self.post_roll_raw(
            content='{"expression":"1d6"}', headers={"content-type": "text/plain"}
        )

        self.assert_public_error(
            response, status_code=415, code="unsupported_media_type"
        )

    async def test_missing_expression_returns_invalid_expression(self) -> None:
        response = await self.post_roll({"seed": 42})

        self.assert_public_error(response, status_code=422, code="invalid_expression")

    async def test_non_string_expression_returns_invalid_expression(self) -> None:
        response = await self.post_roll({"expression": 123, "seed": 42})

        self.assert_public_error(response, status_code=422, code="invalid_expression")

    async def test_unsupported_expression_returns_invalid_expression(self) -> None:
        response = await self.post_roll({"expression": "2d6+1d4", "seed": 42})

        self.assert_public_error(response, status_code=422, code="invalid_expression")

    async def test_non_integer_seed_returns_invalid_seed(self) -> None:
        response = await self.post_roll({"expression": "1d6", "seed": "42"})

        self.assert_public_error(response, status_code=422, code="invalid_seed")

    async def test_limit_failure_returns_limit_metadata(self) -> None:
        response = await self.post_roll({"expression": "1001d6", "seed": 42})

        self.assert_public_error(
            response,
            status_code=422,
            code="expression_limit_exceeded",
            limit=1000,
            actual=1001,
        )

    async def post_roll(self, payload: dict[str, object]) -> httpx.Response:
        return await self.post_roll_raw(json=payload)

    async def post_roll_raw(self, **kwargs: object) -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            return await client.post("/roll", **kwargs)

    def assert_public_error(
        self,
        response: httpx.Response,
        *,
        status_code: int,
        code: str,
        limit: int | None = None,
        actual: int | None = None,
    ) -> None:
        self.assertEqual(response.status_code, status_code)
        body = response.json()
        self.assertEqual(body["status"], status_code)
        self.assertEqual(body["code"], code)
        for field in ("type", "title", "detail"):
            self.assertIsInstance(body[field], str)
            self.assertTrue(body[field])
        if limit is None:
            self.assertNotIn("limit", body)
            self.assertNotIn("actual", body)
        else:
            self.assertEqual(body["limit"], limit)
            self.assertEqual(body["actual"], actual)


if __name__ == "__main__":
    unittest.main()

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

    async def post_roll(self, payload: dict[str, object]) -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            return await client.post("/roll", json=payload)


if __name__ == "__main__":
    unittest.main()

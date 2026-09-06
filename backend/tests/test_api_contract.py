"""API contract tests mirroring openspec dice-api scenarios."""

import unittest

import httpx

from dice_api.main import app


class DiceApiContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_health_endpoint_healthy_service(self) -> None:
        response = await self.request("GET", "/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    async def test_roll_a_dice_group_with_modifier(self) -> None:
        response = await self.roll({"expression": "2d10 + 3", "seed": 123})

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["expression"], "2d10+3")
        self.assertEqual(body["group"]["count"], 2)
        self.assertEqual(body["group"]["sides"], 10)
        self.assertEqual(body["modifier"], 3)

    async def test_reject_unsupported_expression_syntax(self) -> None:
        unsupported_expressions = (
            "2d6+1d4",
            "(1d6)",
            "2d20kh1",
            "not dice",
        )

        for expression in unsupported_expressions:
            with self.subTest(expression=expression):
                response = await self.roll({"expression": expression, "seed": 123})

                self.assert_error(response, status_code=422, code="invalid_expression")

    async def test_return_individual_values_and_total(self) -> None:
        response = await self.roll({"expression": "4d12 - 5", "seed": 123})

        self.assertEqual(response.status_code, 200)
        body = response.json()
        values = body["group"]["values"]
        self.assertEqual(len(values), 4)
        self.assertTrue(all(isinstance(value, int) for value in values))
        self.assertTrue(all(1 <= value <= 12 for value in values))
        self.assertEqual(body["group"]["subtotal"], sum(values))
        self.assertEqual(body["modifier"], -5)
        self.assertEqual(body["total"], body["group"]["subtotal"] - 5)

    async def test_replay_a_seeded_roll(self) -> None:
        first = await self.roll({"expression": "3d8 + 1", "seed": 98765})
        second = await self.roll({"expression": "3d8 + 1", "seed": 98765})

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        first_body = first.json()
        second_body = second.json()
        self.assertEqual(first_body["rng_version"], "v1")
        self.assertEqual(first_body["rng_version"], second_body["rng_version"])
        self.assertEqual(first_body["group"]["values"], second_body["group"]["values"])
        self.assertEqual(first_body["group"]["subtotal"], second_body["group"]["subtotal"])
        self.assertEqual(first_body["total"], second_body["total"])

    async def test_replay_an_unseeded_roll(self) -> None:
        unseeded = await self.roll({"expression": "1d20"})

        self.assertEqual(unseeded.status_code, 200)
        body = unseeded.json()
        self.assertIsInstance(body["seed"], int)
        self.assertEqual(body["rng_version"], "v1")

        replayed = await self.roll({"expression": body["expression"], "seed": body["seed"]})

        self.assertEqual(replayed.status_code, 200)
        self.assertEqual(replayed.json()["rng_version"], body["rng_version"])
        self.assertEqual(replayed.json()["group"]["values"], body["group"]["values"])
        self.assertEqual(replayed.json()["group"]["subtotal"], body["group"]["subtotal"])
        self.assertEqual(replayed.json()["total"], body["total"])

    async def test_invalid_seed(self) -> None:
        response = await self.roll({"expression": "1d6", "seed": "abc"})

        self.assert_error(response, status_code=422, code="invalid_seed")

    async def test_excessive_dice_count(self) -> None:
        response = await self.roll({"expression": "1001d6", "seed": 123})

        self.assert_error(
            response,
            status_code=422,
            code="expression_limit_exceeded",
            limit=1000,
            actual=1001,
        )

    async def test_invalid_die_sides(self) -> None:
        response = await self.roll({"expression": "1d1", "seed": 123})

        self.assert_error(response, status_code=422, code="invalid_expression")

    async def roll(self, payload: dict[str, object]) -> httpx.Response:
        return await self.request("POST", "/roll", json=payload)

    async def request(self, method: str, path: str, **kwargs: object) -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            return await client.request(method, path, **kwargs)

    def assert_error(
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
        if limit is not None:
            self.assertEqual(body["limit"], limit)
            self.assertEqual(body["actual"], actual)


if __name__ == "__main__":
    unittest.main()

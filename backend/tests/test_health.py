"""Endpoint tests for the service health check."""

import unittest

import httpx

from dice_api.main import app


class HealthEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def test_ready_service_returns_ok_status(self) -> None:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            response = await client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()

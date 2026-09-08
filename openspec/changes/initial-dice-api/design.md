# Design: initial-dice-api

- Python 3.12, FastAPI, pydantic v2 для валидации (границы задаются в модели запроса).
- Генератор: `random.Random(seed)`; если seed не передан — берём `secrets.randbits(32)` и возвращаем его в ответе.
- Ошибки валидации — стандартные 422 FastAPI; текст detail должен содержать имя поля.
- Тесты: pytest + httpx `TestClient`.
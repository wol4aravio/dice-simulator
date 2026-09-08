## 1. Backend package metadata

- [ ] 1.1 Убедиться, что `backend/pyproject.toml` содержит installable project с `[project].name = "dice-simulator-backend"` и semver `[project].version`, и проверить через `cd backend && uv run python -c "from importlib.metadata import version; print(version('dice-simulator-backend'))"`

## 2. Health endpoint version source

- [ ] 2.1 Реализовать получение версии `/health` через `importlib.metadata.version('dice-simulator-backend')` в одном месте backend-кода и проверить, что в реализации нет хардкода значения версии
- [ ] 2.2 Подключить metadata-derived version к ответу `GET /health` без изменения формы JSON и проверить вручную через `cd backend && uv run pytest` или существующий health test

## 3. Tests

- [ ] 3.1 Добавить/обновить тест `GET /health`, который сравнивает `response.json()["version"]` с `importlib.metadata.version('dice-simulator-backend')`, и проверить падение теста невозможно устранить хардкодом конкретной версии
- [ ] 3.2 Запустить `cd backend && uv run pytest` и убедиться, что health tests и существующие backend tests проходят

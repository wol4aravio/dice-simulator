## Context

В репозитории пока нет реализованного backend-кода: `backend/` содержит только placeholder. Активный change `initial-dice-api` уже вводит `GET /health` и backend skeleton, поэтому этот change должен быть применён совместно с ним или сразу после него, без создания второго независимого health endpoint.

## Goals / Non-Goals

**Goals:**
- Сделать `[project].version` в `backend/pyproject.toml` единственным источником версии backend-сервиса.
- Получать версию для `/health` через Python package metadata: `importlib.metadata.version(...)`.
- Проверять в тестах совпадение `/health.version` с package metadata, а не с хардкод-литералом.

**Non-Goals:**
- Не вводить отдельную версию API, отличную от версии backend-пакета.
- Не добавлять build-time генерацию файлов версии.
- Не читать `pyproject.toml` напрямую в runtime-коде приложения.
- Не менять JSON-формат ответа `/health` сверх источника значения `version`.

## Decisions

### Использовать `importlib.metadata.version(...)`

Решение: реализация `/health` получает версию установленного backend distribution package через `importlib.metadata.version(<distribution-name>)`.

Рationale:
- Это стандартный механизм Python для чтения версии установленного пакета.
- Runtime-код не зависит от наличия `pyproject.toml` в рабочей директории или Docker image.
- Источником истины остаётся `[project].version` в `backend/pyproject.toml`, а package metadata создаётся инструментами упаковки.

Альтернативы:
- Читать `backend/pyproject.toml` через `tomllib`: проще в неустановленном checkout, но привязывает runtime к файлу и путям.
- Держать `__version__` в коде: проще, но создаёт второй источник истины.
- Генерировать `_version.py` на build step: надёжно в runtime, но избыточно для минимального API и добавляет процесс генерации.

### Зафиксировать distribution name в package metadata

Решение: backend project должен иметь стабильное имя distribution package в `backend/pyproject.toml`, например `dice-simulator-backend`. Реализация `/health` использует ровно это имя при вызове `version(...)`.

Рationale:
- `importlib.metadata.version(...)` работает по имени distribution package, а не по имени import package.
- Явное имя делает тесты и runtime-поведение предсказуемыми.

### Тестировать через metadata, а не литерал

Решение: тест `/health` вычисляет ожидаемую версию через тот же источник package metadata и сравнивает её с `response.json()["version"]`.

Рationale:
- Тест не должен закреплять конкретное значение вроде `"0.1.0"`.
- При изменении `[project].version` тест продолжит проверять связь с источником истины.

## Risks / Trade-offs

- [Risk] `PackageNotFoundError` при запуске приложения без установленного backend-пакета → Mitigation: backend skeleton должен быть installable project, а локальные команды и тесты выполняются через `uv run` из `backend/`.
- [Risk] Несовпадение distribution name и import package name → Mitigation: явно задокументировать distribution name в `pyproject.toml` и использовать его в одном месте в коде.
- [Risk] Пересечение с `initial-dice-api` по `/health` → Mitigation: при применении сначала согласовать task `1.1`/`1.2` так, чтобы `/health` сразу реализовывался с package metadata, без промежуточного хардкода.

## Migration Plan

Так как backend ещё не реализован, миграция данных или обратная совместимость не требуются. При реализации нужно создать package metadata в рамках backend skeleton и сразу подключить её к `/health`.

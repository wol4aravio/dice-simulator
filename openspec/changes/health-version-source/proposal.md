# Proposal: health-version-source

Proposed at 2026-09-08T04:49:50Z

## Why

`GET /health` должен возвращать версию сервиса из единого источника, чтобы избежать рассинхронизации между метаданными пакета и ответом API. Это важно сейчас, пока `initial-dice-api` ещё задаёт базовый backend skeleton и endpoint `/health`.

## What Changes

- Уточнить поведение `GET /health`: поле `version` соответствует версии backend-пакета, объявленной в `[project].version` в `backend/pyproject.toml`.
- Использовать стандартный механизм Python package metadata через `importlib.metadata.version(...)`, а не хардкод версии в коде приложения.
- Добавить проверку, что `/health.version` совпадает с версией установленного backend distribution package.
- Не менять формат ответа `/health`: `status` остаётся `"ok"`, `version` остаётся semver-строкой.

## Capabilities

### New Capabilities
- `dice-api`: уточняет контракт health endpoint для capability, вводимого активным change `initial-dice-api`, до появления основной спеки в `openspec/specs/`.

### Modified Capabilities
- Нет: в основной директории `openspec/specs/` пока нет существующего capability для изменения.

## Impact

- Backend package metadata: `backend/pyproject.toml` должен содержать корректные `[project].name` и `[project].version`.
- Backend application code: реализация `/health` должна получать версию через `importlib.metadata.version(<backend-distribution-name>)`.
- Backend tests: тест `/health` должен сравнивать ответ с package metadata, а не с литералом в коде.
- Активный change `initial-dice-api`: пересекается с задачами `1.1` и `1.2`; при применении changes нужно избежать двух разных реализаций `/health`.

# Proposal: initial-dice-api

## Why
Нужен минимальный HTTP API для броска костей как основа для frontend, CLI.

## What changes
- Новый capability `dice-api`: `GET /health`, `POST /roll`.
- Валидация входа с явными границами.
- Воспроизводимость через `seed`.

## Out of scope
- Выражения `NdS+M`, история бросков, аутентификация.

## Risks
- Слишком широкий API затянет остальные уроки; держим ровно два endpoint-а.

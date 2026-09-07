# Dice Simulator

Данный проект является учебным и создан в рамках процесса изучения различных подходов при работе с ИИ-агентами.

Основной функционал заключается в создании:
- API для генерации результатов бросков по запросу
- Web UI для взаимодействия через веб-интерфейс
- CLI-утилиту для вызова через терминал

## ver 1.0 scope
- GET /health → {"status":"ok","version":"<semver>"}
- POST /roll {dice, sides, seed?} → {rolls[], total, dice, sides, seed}
- Ограничения: 1 ≤ dice ≤ 100; 2 ≤ sides ≤ 100; seed — целое, опционально
- Валидация: 422 с понятным detail
- Frontend: форма dice/sides, кнопка Roll, вывод rolls и total
- CLI: `dice roll`, `dice health`
- Docker: compose с healthcheck

## Сознательно отложено
- выражения `NdS+M` (появятся как OpenSpec change)
- история бросков, статистика
- аутентификация, персистентность, i18n


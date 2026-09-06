# 0001-design-dice-api

Date: 2026-09-06 14:29:28 UTC

## Why

The simulator needs one stable dice-roll contract shared by its future API, Web UI, and CLI. Defining its inputs, deterministic behavior, errors, and resource limits before implementation prevents clients from depending on accidental behavior.

## What Changes

- Add a health-check endpoint contract for service availability.
- Add a dice-roll endpoint that accepts a bounded `NdM`, optionally with an integer modifier, and returns individual die values and the total.
- Define optional seed behavior so a supplied seed reproduces a roll and an omitted seed is generated and returned for replay.
- Define JSON error responses and request-expression limits.
- Limit the initial expression language to one dice group and an optional `+K` or `-K` modifier; advanced dice notation is out of scope.

## Capabilities

### New Capabilities
- `dice-api`: HTTP health and dice-roll API behavior, including validation, deterministic seeded rolls, error responses, and limits.

### Modified Capabilities
- None.

## Impact

- A future FastAPI backend will expose `GET /health` and `POST /roll`.
- The Web UI and CLI can use the same roll request and response contract.
- Implementation will require expression parsing, validation, a versioned deterministic random-number generator, and API tests.

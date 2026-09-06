## Purpose

Define a stable HTTP contract for health checks and reproducible, bounded dice rolls shared by all simulator clients.

## ADDED Requirements

### Requirement: Health endpoint
The system SHALL expose `GET /health` and respond with HTTP 200 and a JSON object whose `status` field is `"ok"` when the API service is ready to accept roll requests.

#### Scenario: Healthy service
- **WHEN** a client sends `GET /health` to a ready service
- **THEN** the service responds with HTTP 200 and `{"status":"ok"}`

### Requirement: Dice roll request
The system SHALL expose `POST /roll` accepting `application/json` with a required `expression` string and an optional integer `seed`. The expression SHALL contain exactly one dice group in the form `NdM`, where `N` and `M` are positive decimal integers, followed optionally by one integer modifier in the form `+K` or `-K`; ASCII whitespace around tokens SHALL be accepted. The endpoint SHALL reject all other dice notation and arithmetic.

#### Scenario: Roll a dice group with a modifier
- **WHEN** a client posts `{"expression":"2d10 + 3"}` to `/roll`
- **THEN** the service responds with HTTP 200 and a result for two ten-sided dice plus a modifier of three

#### Scenario: Reject unsupported expression syntax
- **WHEN** a client posts an expression with multiple dice groups, parentheses, keep/drop notation, or invalid syntax
- **THEN** the service responds with HTTP 422 and an `invalid_expression` error

### Requirement: Dice roll result
For a valid roll request, the system SHALL respond with HTTP 200 and JSON containing: the normalized expression; the seed used; one roll group containing `count`, `sides`, `values`, and `subtotal`; the signed `modifier`; and the final `total`. Each value SHALL be an integer from 1 through the requested number of sides inclusive, `subtotal` SHALL equal the sum of `values`, and `total` SHALL equal `subtotal + modifier`.

#### Scenario: Return individual values and total
- **WHEN** a valid expression is rolled
- **THEN** every generated die value, its subtotal, the modifier, and the calculated total are present and arithmetically consistent

### Requirement: Reproducible seeded rolls
When a valid integer `seed` is supplied, the system SHALL use it to produce the same response roll values for the same normalized expression and RNG version. When no seed is supplied, the system SHALL generate a seed, use it for the roll, and return it in the response. The response SHALL include an `rng_version` identifier.

#### Scenario: Replay a seeded roll
- **WHEN** a client submits the same valid expression and seed twice to the same RNG version
- **THEN** both successful responses contain identical roll values, subtotals, and totals

#### Scenario: Replay an unseeded roll
- **WHEN** a client submits a valid expression without a seed
- **THEN** the successful response contains the generated seed and submitting that expression with the returned seed reproduces the roll for the same RNG version

### Requirement: Validation errors
The system SHALL return JSON errors with `type`, `title`, `status`, `detail`, and stable machine-readable `code` fields. Invalid JSON SHALL return HTTP 400 with `invalid_json`; an unsupported content type SHALL return HTTP 415 with `unsupported_media_type`; invalid seeds or syntactically invalid expressions SHALL return HTTP 422 with `invalid_seed` or `invalid_expression` respectively.

#### Scenario: Invalid seed
- **WHEN** a client posts a non-integer seed in otherwise valid JSON
- **THEN** the service responds with HTTP 422 and an error whose `code` is `invalid_seed`

### Requirement: Roll resource limits
The system SHALL enforce these limits: expression length of at most 256 characters, at most 1,000 dice per request, dice sides from 2 through 1,000,000 inclusive, and absolute modifier at most 1,000,000,000. A validly formed expression that exceeds a limit SHALL return HTTP 422 with an `expression_limit_exceeded` error that includes `limit` and `actual` fields.

#### Scenario: Excessive dice count
- **WHEN** a client requests 1001 dice in a syntactically valid expression
- **THEN** the service responds with HTTP 422 and `expression_limit_exceeded` without generating dice values

#### Scenario: Invalid die sides
- **WHEN** a client requests a die with fewer than two sides
- **THEN** the service responds with HTTP 422 and an `invalid_expression` error

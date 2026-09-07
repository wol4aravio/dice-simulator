## ADDED Requirements

### Requirement: Health endpoint
The service SHALL expose `GET /health` returning HTTP 200 and a JSON body with `status` equal to `"ok"` and a semver `version`.

#### Scenario: Service is up
- **WHEN** a client requests `GET /health`
- **THEN** the response status is 200 and body contains `{"status": "ok", "version": "<semver>"}`

### Requirement: Roll dice
The service SHALL accept `POST /roll` with JSON body `{dice, sides, seed?}` and return individual rolls and their total.

#### Scenario: Valid roll
- **WHEN** the body is `{"dice": 2, "sides": 6}`
- **THEN** status is 200 and body contains `rolls` (list of 2 integers, each in [1, 6]), `total` equal to the sum, and echoes `dice` and `sides`

#### Scenario: Reproducible roll
- **WHEN** the same body with `"seed": 42` is sent twice
- **THEN** both responses contain identical `rolls`

#### Scenario: Missing seed
- **WHEN** `seed` is omitted
- **THEN** the response contains the actually used `seed` as an integer, so a roll can be reproduced later

### Requirement: Input validation
The service SHALL reject invalid input with HTTP 422 and a `detail` describing the violated constraint. Constraints: `1 <= dice <= 100`, `2 <= sides <= 100`, `seed` is an integer if present.

#### Scenario: Too many dice
- **WHEN** the body is `{"dice": 101, "sides": 6}`
- **THEN** status is 422 and `detail` mentions the `dice` limit

#### Scenario: Wrong type
- **WHEN** the body is `{"dice": "two", "sides": 6}`
- **THEN** status is 422

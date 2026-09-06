## 1. Backend foundation

- [x] 1.1 Initialize the Python/FastAPI backend package and application entry point, and verify the application starts locally with the project package manager.
- [x] 1.2 Define typed roll request, successful response, roll-group, and public error-envelope models, and verify serialization tests match the `dice-api` spec.

## 2. Roll domain logic

- [x] 2.1 Implement parsing and normalization for one `NdM` expression with an optional signed modifier, and verify table-driven tests accept documented syntax and reject unsupported notation.
- [x] 2.2 Implement pre-execution validation for expression length, dice count, sides, modifier, and seed bounds, and verify every limit produces the specified HTTP error code when integrated.
- [x] 2.3 Implement versioned deterministic seeded rolling plus entropy-backed seed generation for unseeded rolls, and verify identical expression/seed pairs reproduce values and totals.

## 3. HTTP endpoints

- [x] 3.1 Add `GET /health` with the specified ready response, and verify an endpoint test receives HTTP 200 and `{"status":"ok"}`.
- [x] 3.2 Add `POST /roll` wired to parsing, validation, and roll execution, and verify endpoint tests cover successful rolls with and without a seed.
- [ ] 3.3 Map invalid JSON, media type, request fields, expression failures, and limit failures to the documented public error envelope, and verify endpoint tests assert status codes and machine-readable error codes.

## 4. Verification and documentation

- [ ] 4.1 Add API contract tests for all scenarios in `specs/dice-api/spec.md`, and verify the full backend test suite passes.
- [ ] 4.2 Publish OpenAPI-visible request, success, and error examples for `/health` and `/roll`, and verify generated API documentation reflects the specified contract.

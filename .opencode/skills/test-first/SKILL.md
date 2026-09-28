---
name: test-first
description: How we add or change behaviour in this repo — write the failing test first, then the code. Use for any feature, bug fix or refactor in apps/backend.
---
# test-first

## Loop
1. Locate the test file for the module (`apps/backend/tests/test_<module>.py`; create it if missing).
2. Write the smallest test that fails for the right reason. Run `make test` and confirm it fails.
3. Implement the minimum code to pass. Run `make test`.
4. Refactor with the tests green. Run `make test` one last time.

## Rules
- Domain tests (`dice/`) never import FastAPI. HTTP tests use `fastapi.testclient.TestClient`.
- Use `@pytest.mark.parametrize` for tables of inputs; one assertion idea per test.
- Error paths are tested by message fragment: `with pytest.raises(ValueError) as e: ...; assert "at least 1" in str(e.value)`.
- Random behaviour is tested with fixed seeds, never with retries.
- Never weaken or delete a test to make it pass; if the test is wrong, say so and fix it explicitly.

## Templates
See `templates.md` in this folder for a parametrized-test and an HTTP-test skeleton.

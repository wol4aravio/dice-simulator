---
description: Full pre-commit check — lint, tests, docker build via the docker-check skill
agent: build
---
Run, in order: `make lint`, `make test`, then follow the `docker-check` skill for the backend.
Stop at the first failure, fix it, and rerun from the start. Finish with a checklist of what passed.
$ARGUMENTS

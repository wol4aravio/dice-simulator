---
name: docker-check
description: Verify that a service builds and its healthcheck passes in Docker Compose. Use after any change to a Dockerfile, compose.yaml, or dependencies.
---
# docker-check

Run `bash .opencode/skills/docker-check/scripts/check.sh <service>` (default service: `backend`).
The script builds the image, starts the service, waits for `/health`, prints the last 20 log lines and
stops the service. Exit code 0 means healthy.

If it fails:
- build error → read the failing layer, fix the Dockerfile or `pyproject.toml`, rerun;
- healthcheck timeout → `docker compose logs <service>`; the usual causes are a wrong module path in `CMD`
  or a missing dependency in `pyproject.toml`;
- port in use → `docker compose down` and rerun.

Do not edit the script to make it pass.

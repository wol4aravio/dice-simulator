#!/usr/bin/env bash
# Build, start, wait for health, show logs, stop. Usage: check.sh [service] [port]
set -euo pipefail
SERVICE="${1:-backend}"
PORT="${2:-8000}"
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
echo "== build $SERVICE"
docker compose build "$SERVICE"
echo "== up $SERVICE"
docker compose up -d "$SERVICE"
trap 'docker compose stop "$SERVICE" >/dev/null' EXIT
echo "== waiting for http://127.0.0.1:$PORT/health"
for i in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    echo "healthy after ${i}s"
    curl -sS "http://127.0.0.1:$PORT/health"; echo
    docker compose logs --tail 20 "$SERVICE"
    exit 0
  fi
  sleep 1
done
echo "!! healthcheck timed out"
docker compose logs --tail 50 "$SERVICE"
exit 1

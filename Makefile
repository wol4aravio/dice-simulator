.PHONY: test lint fmt up down check
BACKEND=apps/backend

test:
	cd $(BACKEND) && uv run pytest -q

lint:
	cd $(BACKEND) && uv run ruff check src tests && uv run ruff format --check src tests

fmt:
	cd $(BACKEND) && uv run ruff format src tests && uv run ruff check --fix src tests

up:
	docker compose up -d --build

down:
	docker compose down

check: lint test
	bash .opencode/skills/docker-check/scripts/check.sh backend

install:
	cd backend && uv sync
	cd frontend && npm install
migrate:
	cd backend && uv run alembic upgrade head
test:
	cd backend && uv run pytest

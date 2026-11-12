.PHONY: backend-install frontend-install backend-test frontend-build run-backend run-frontend docker-up

backend-install:
	cd backend && python -m venv .venv && .venv/Scripts/python -m pip install -U pip && .venv/Scripts/python -m pip install -e ".[dev]"

frontend-install:
	cd frontend && npm install

backend-test:
	cd backend && .venv/Scripts/python -m pytest -q

frontend-build:
	cd frontend && npm run build

run-backend:
	cd backend && .venv/Scripts/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build

# Contributing

1. Read `AGENTS.md`, `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE.md`, and `docs/DECISIONS.md`.
2. Respect file ownership in `docs/AGENT_OWNERSHIP.md`.
3. Prefer small, tested vertical slices.
4. Run relevant tests before opening a PR.
5. Keep scientific honesty: label simulator vs QPU vs classical sources correctly.
6. Do not commit secrets.
7. If you change hosts or public URLs, update `README.md`, `docs/DEPLOYMENT.md`, `docs/DEMO_SCRIPT.md`, and related docs.

## Live reference

| Surface | URL |
|---|---|
| App | https://qubitkey.vercel.app |
| API | https://qubitkey-backend.onrender.com |
| Docs index | [`docs/README.md`](docs/README.md) |

## Development

```bash
# Backend
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

Optional: point a local frontend at the hosted API with `VITE_API_BASE=https://qubitkey-backend.onrender.com`.

## Pull requests

Include: changed files, commands run, test results, and known limitations. Never claim hardware execution or visual QA without evidence. Do not claim production security certification.

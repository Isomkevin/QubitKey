# Contributing

1. Read `AGENTS.md`, `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE.md`, and `docs/DECISIONS.md`.
2. Respect file ownership in `docs/AGENT_OWNERSHIP.md`.
3. Prefer small, tested vertical slices.
4. Run relevant tests before opening a PR.
5. Keep scientific honesty: label simulator vs QPU vs classical sources correctly.
6. Do not commit secrets.

## Development

```bash
# Backend
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Pull requests

Include: changed files, commands run, test results, and known limitations. Never claim hardware execution or visual QA without evidence.

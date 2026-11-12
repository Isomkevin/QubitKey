# QubitKey Agent Ownership

Disjoint file ownership prevents concurrent edit conflicts. Agents use separate branches or worktrees. Shared schema changes require Coordinator approval and an ADR in `docs/DECISIONS.md`.

## Ownership matrix

| Agent | Role | Owns exclusively | Must not modify |
|---|---|---|---|
| **0** | Coordinator / Architect | `docs/IMPLEMENTATION_PLAN.md`, `docs/AGENT_OWNERSHIP.md`, `docs/INTEGRATION_CONTRACTS.md`, `docs/DECISIONS.md`; `backend/app/schemas/`; `backend/app/core/`; `backend/app/main.py`; `backend/app/api/__init__.py`; `backend/app/api/health.py`; `backend/app/api/config.py` | Feature bodies inside quantum/analysis/security/frontend during their active milestones |
| **1** | Quantum Engine | `backend/app/quantum/`; `backend/app/api/qrng.py`; `backend/app/api/experiments.py`; `notebooks/`; `backend/tests/test_quantum*.py`; `backend/tests/test_qrng*.py`; `backend/tests/test_experiments*.py` | `backend/app/analysis/`, `backend/app/security/`, `frontend/` |
| **2** | Analysis | `backend/app/analysis/`; `backend/app/api/analysis.py`; `backend/tests/test_analysis*.py` | `backend/app/quantum/`, `backend/app/security/`, `frontend/` |
| **3** | Frontend | `frontend/**` | Backend source (consume OpenAPI/contracts only) |
| **4** | Security / Auth | `backend/app/security/`; `backend/app/api/totp.py`; `backend/app/api/pqc.py`; `docs/THREAT_MODEL.md`; `backend/tests/test_totp*.py`; `backend/tests/test_pqc*.py`; `backend/tests/test_security*.py` | `backend/app/quantum/`, `backend/app/analysis/`, frontend crypto logic |
| **5** | QA / Release | `.github/`; `docker-compose.yml`; `Makefile`; `SECURITY.md`; `CONTRIBUTING.md`; `docs/EXPERIMENT_METHODOLOGY.md`; `docs/DEMO_SCRIPT.md`; root packaging helpers; E2E checklists | Architecture rewrites without ADR |

## Shared / root files

| Path | Owner | Notes |
|---|---|---|
| `README.md` | Agent 5 (with Coordinator review) | Fix structure/commands to match `backend.app.main:app` |
| `.env.example` | Agent 0 initially; Agent 5 maintains | No secrets |
| `.gitignore` | Agent 0 initially; Agent 5 maintains | |
| `backend/pyproject.toml` | Agent 0 scaffolds; domain agents propose deps via ADR | Coordinator merges dependency pins |
| `LICENSE` | Human / Coordinator | MIT; do not alter without approval |
| `AGENTS.md` | Coordinator | Mission rules |

## Parallelism rules

1. **One owner per path.** Do not edit another agent's files without explicit handoff.
2. **Branch naming:** `m1-quantum`, `m2-analysis`, `m3-frontend`, `m4-security`, `m5-ibm`, `m6-pqc`, `m7-release`.
3. **Schema freeze:** `backend/app/schemas/` is Coordinator-owned. Other agents import models; they do not mutate fields without an ADR + contract update.
4. **API route files** are split by domain (`qrng.py`, `analysis.py`, `totp.py`, …). Router registration stays in Coordinator-owned `main.py`.
5. **Frontend fixtures:** Allowed only behind a development flag and must be labelled as fixtures until Milestone 1 API is live.
6. **Handoff report required** from every agent: changed files, commands run, test results, limitations, honesty checklist.

## Milestone → primary agent

| Milestone | Primary | Supporting |
|---|---|---|
| 0 Planning docs | 0 | — |
| 1 QRNG slice | 1 | 0 (scaffold/schemas) |
| 2 Analysis + notebook | 2 | 1 (notebook) |
| 3 Frontend lab | 3 | 0 (contract clarifications) |
| 4 TOTP | 4 | 3 (UI wire-up) |
| 5 IBM adapter | 1 | 3 (hardware availability UI) |
| 6 ML-DSA stretch | 4 | 3 (experimental page) |
| 7 Release | 5 | all |

## Conflict resolution

1. Stop concurrent edits on the contested path.
2. Coordinator decides ownership or sequences the work.
3. Record the decision in `docs/DECISIONS.md`.
4. Rebase/merge only after tests pass on the owning agent's branch.

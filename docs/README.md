# QubitKey Documentation

Judge- and contributor-facing documentation for the AstraCode Qiskit Fall Fest 2026 submission.

## Live platform

| Surface | URL |
|---|---|
| Web app (Vercel) | https://qubitkey.vercel.app |
| API (Render) | https://qubitkey-backend.onrender.com |
| OpenAPI | https://qubitkey-backend.onrender.com/docs |
| Health | https://qubitkey-backend.onrender.com/api/health |
| Research notebook (Binder, latest) | https://mybinder.org/v2/gh/Isomkevin/QubitKey/main?labpath=notebooks%2Fqrng_experiments.ipynb |
| Research notebook (Binder, pinned) | https://mybinder.org/v2/gh/Isomkevin/QubitKey/ef87d4e1390975de631c5dfc7a69f4c00d1244c2?urlpath=lab%2Ftree%2Fnotebooks%2Fqrng_experiments.ipynb |
| Repository | https://github.com/Isomkevin/QubitKey |

Cold start note: the free Render backend may sleep after ~15 minutes idle. Allow 30–60 seconds on the first request after wake. Binder sessions are temporary; always share a `mybinder.org/v2/...` launch URL, not a `hub.*.mybinder.org/user/...` session link. Prefer the pinned Binder URL for reproducible judging.

## Start here (judges)

1. Open the [live app](https://qubitkey.vercel.app).
2. Follow the timed walkthrough in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).
3. Optional: open the [pinned research notebook on Binder](https://mybinder.org/v2/gh/Isomkevin/QubitKey/ef87d4e1390975de631c5dfc7a69f4c00d1244c2?urlpath=lab%2Ftree%2Fnotebooks%2Fqrng_experiments.ipynb) and run cells top-to-bottom.
4. Skim scientific honesty in [`EXPERIMENT_METHODOLOGY.md`](EXPERIMENT_METHODOLOGY.md) and [`THREAT_MODEL.md`](THREAT_MODEL.md).

## Document map

| Document | Purpose |
|---|---|
| [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) | ~8 minute judged demo script (hosted + local) |
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Render + Vercel deployment, env vars, ops notes |
| [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) | Product goals, MVP scope, acceptance criteria |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Components, data flow, trust boundaries, hosting |
| [`INTEGRATION_CONTRACTS.md`](INTEGRATION_CONTRACTS.md) | Frozen API contracts and provenance rules |
| [`EXPERIMENT_METHODOLOGY.md`](EXPERIMENT_METHODOLOGY.md) | How QRNG experiments are defined and interpreted |
| [`THREAT_MODEL.md`](THREAT_MODEL.md) | Assets, threats, mitigations, non-goals |
| [`DECISIONS.md`](DECISIONS.md) | Architecture decision records |
| [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) | Milestone plan |
| [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) | Fresh-clone and hosted verification checklist |
| [`AGENT_OWNERSHIP.md`](AGENT_OWNERSHIP.md) | Multi-agent file ownership |

## Scientific honesty (non-negotiable)

- Qiskit Aer output is **simulated**, not physical quantum entropy.
- IBM QPU output is physical measurement data only when a real job runs — never silently substituted with a simulator.
- **QRNG ≠ post-quantum cryptography.**
- **TOTP ≠ quantum-resistant.**
- Passing statistical tests ≠ cryptographic security or entropy certification.

## Local reproduction

See the root [`README.md`](../README.md) and [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md). Research notebooks: [`../notebooks/README.md`](../notebooks/README.md).

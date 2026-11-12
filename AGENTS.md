# AGENTS.md — QubitKey

## Mission
Build a scientifically honest, secure-by-design, open-source QRNG education and TOTP demonstration.

## Live demo (do not invent alternate public URLs)
- App: https://qubitkey.vercel.app
- API: https://qubitkey-backend.onrender.com
- Docs index: `docs/README.md` · Deployment: `docs/DEPLOYMENT.md`

## Mandatory truthfulness
- Qiskit simulator output is simulated; never call it genuine physical quantum entropy.
- Hardware output requires a real IBM backend execution and verifiable job metadata.
- QRNG is not post-quantum cryptography.
- TOTP is not quantum-resistant.
- Statistical test success is not proof of cryptographic security.
- Never claim entropy certification or production security without evidence.

## Engineering
- Inspect before editing.
- Prefer small, testable vertical slices.
- JavaScript preferred for frontend unless TypeScript is justified.
- Python for quantum/backend.
- Use maintained libraries; no custom cryptography.
- Pin compatible dependencies and verify official current APIs.
- Add tests for every meaningful feature.
- Keep docs in sync with behavior.
- No secrets in Git, logs, screenshots or frontend storage.
- Never silently fall back from IBM QPU to simulator.
- Ask before adding paid services, cloud dependencies or external storage.

## Agent collaboration
- Respect assigned file ownership.
- Use branches/worktrees for parallel work.
- Do not edit another agent's files without coordination.
- Report changed files, commands run, test results and limitations.
- Do not claim visual QA or hardware execution unless actually performed.

## Definition of done
A feature runs, tests pass, acceptance criteria are met, security implications are documented, and the human can reproduce it from a clean checkout.

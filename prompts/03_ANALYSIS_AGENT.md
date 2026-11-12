# Analysis Agent Prompt

Implement only `backend/app/analysis/` and its tests.

Implement frequency proportions, integer histograms, longest run, run-length summaries, empirical Shannon entropy, lagged autocorrelation and appropriately caveated goodness-of-fit diagnostics.

Compare equal sample sizes from:
- Qiskit simulator (educational)
- Python `random.Random` (educational PRNG)
- Python `secrets` (classical CSPRNG)
- IBM QPU only when real hardware data is supplied

Requirements:
- Deterministic fixtures for tests.
- Never claim statistical tests prove cryptographic security.
- Do not cherry-pick or suppress inconvenient results.
- Explain assumptions and expected-count limitations.
- Do not implement NIST 90B min-entropy certification.
- Agree on stable response models with coordinator before coding.

Return formulas, limitations, commands run, tests and example report.

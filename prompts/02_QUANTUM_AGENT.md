# Quantum Engine Agent Prompt

Implement only the Qiskit quantum engine and notebook, following `AGENTS.md`, `docs/PRODUCT_SPEC.md` and `docs/ARCHITECTURE.md`.

Scope:
- Hadamard circuit builder.
- Measurement and bit-order-safe conversion.
- Local simulator adapter using a currently supported Qiskit API.
- Optional IBM Quantum Runtime adapter behind explicit configuration.
- Provenance metadata and clear errors.
- Runnable `notebooks/qrng_experiment.ipynb`.

Requirements:
- Default path works without IBM credentials.
- Simulator is always labelled educational simulation, not physical quantum entropy.
- Never silently fall back from QPU to simulator.
- Add tests for circuit shape, counts, conversion, shots, qubits, output schema and missing credentials.
- Check official current Qiskit documentation and pin compatible versions.
- Do not implement cryptographic entropy claims or secret generation in this scope.

Return implementation notes, commands run, tests and limitations.

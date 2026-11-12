# QubitKey

### Quantum Entropy. Stronger Digital Identity.

**An open-source quantum entropy laboratory and authentication prototype built with IBM Qiskit.**

[![Built with Qiskit](https://img.shields.io/badge/Built%20with-Qiskit-6929C4)](https://www.ibm.com/quantum/qiskit)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

QubitKey explores how quantum computing can contribute to the future of digital security by combining **quantum random number generation (QRNG), entropy analysis, and practical digital authentication** in one interactive platform.

Built for the **AstraCode Qiskit Fall Fest 2026 Hackathon**, QubitKey translates quantum computing concepts into an accessible, experiment-driven security application.

---

## The Idea

Randomness is fundamental to modern cryptography. It underpins cryptographic keys, authentication secrets, nonces, and other security-critical values.

Conventional software random number generators rely on deterministic algorithms or operating-system entropy sources. Quantum mechanics offers another approach: measurement outcomes from appropriately prepared quantum states can provide inherently probabilistic results.

QubitKey investigates this concept through Qiskit.

The platform prepares qubits in superposition using Hadamard gates, measures their states, and converts the resulting bitstrings into numerical samples. It then provides tools to inspect and analyse the generated outcomes.

We connect this experimental foundation to a practical authentication workflow using Time-Based One-Time Passwords (TOTP).

The result is a platform that brings together quantum experimentation, statistical analysis, and an understandable digital identity security use case.

## Core Features

### 1. Quantum Random Number Generation

Generate random binary outcomes using Qiskit quantum circuits.

The core experiment:

1. Initialise qubits in the computational basis state \(|0\rangle\).
2. Apply Hadamard gates to place the qubits into superposition.
3. Measure the qubits in the computational basis.
4. Collect measurement outcomes.
5. Convert the resulting bitstrings into numerical samples.

The platform supports configurable circuit experiments and repeated measurements, subject to backend limits.

### 2. Entropy Observatory

Explore the statistical characteristics of generated samples through interactive visualisations and analytical tools.

Metrics include:

- Bit frequency and distribution.
- Zero-to-one balance.
- Outcome histograms.
- Longest runs and run-length behaviour.
- Empirical Shannon entropy.
- Autocorrelation.
- Frequency and goodness-of-fit analysis.

These measurements help users understand the behaviour of generated samples and compare different randomness sources.

**Important:** Statistical tests can identify certain patterns and deviations. Passing them does not establish cryptographic security or prove that a source contains sufficient min-entropy.

### 3. Randomness Comparison

QubitKey provides a framework for comparing different randomness sources:

| Source | Description |
|---|---|
| Qiskit Aer | Classical simulation of quantum circuits |
| IBM Quantum hardware | Physical quantum circuit execution, where available |
| Python `random` | Deterministic pseudorandom number generation |
| Python `secrets` | Operating-system-backed cryptographically secure randomness |

Comparisons are performed using equivalent sample sizes and documented experimental settings.

This distinction matters: a quantum circuit simulated on a classical computer does not produce physical quantum randomness.

### 4. Authenticator

QubitKey connects its experimental work to a practical authentication application.

The authenticator demonstrates:

- TOTP enrollment.
- QR-code provisioning.
- Authenticator-compatible secret provisioning.
- Time-based one-time password generation and verification.
- Invalid and expired code handling.

The implementation uses established authentication standards and maintained cryptographic libraries rather than custom cryptographic algorithms.

### 5. Post-Quantum Cryptography Exploration

QubitKey provides an architectural foundation for exploring post-quantum digital identity.

A possible extension is an isolated demonstration of **ML-DSA (Module-Lattice-Based Digital Signature Algorithm)**, a standardised post-quantum digital signature scheme.

This is distinct from QRNG and TOTP:

- QRNG concerns the generation of random measurement outcomes.
- TOTP provides time-based one-time password authentication.
- ML-DSA provides digital signatures designed to resist attacks from quantum-capable adversaries.

These technologies solve different problems and should not be conflated.

---

## How It Works

The core quantum experiment uses a Hadamard transformation.

For a single qubit:

\[
H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
\]

This prepares an equal superposition of the computational basis states.

When measured, the idealised circuit produces:

- `0` with probability 50%.
- `1` with probability 50%.

For multiple qubits, applying Hadamard gates independently creates a superposition of computational basis states. Measurement produces a bitstring that can be converted into a numerical sample.

For example:

```text
Quantum measurement: 10110101

Binary: 10110101
Decimal: 181
```

Repeated measurements generate datasets that can be analysed statistically.

### Experimental Workflow

```text
Configure Experiment
        |
        v
Prepare Quantum Circuit
        |
        v
Apply Hadamard Gates
        |
        v
Measure Qubits
        |
        v
Collect Measurement Outcomes
        |
        v
Analyse Entropy and Distribution
        |
        v
Visualise and Export Results
```

---

## Architecture

QubitKey follows a modular architecture that separates the user interface, quantum execution, statistical analysis, and authentication functionality.

```text
                 QUBITKEY PLATFORM
                        |
          +-------------+-------------+
          |                           |
          v                           v
    React Frontend              FastAPI Backend
          |                           |
          |              +------------+------------+
          |              |            |            |
          v              v            v            v
     Quantum Lab      QRNG Engine  Analysis    Authenticator
          |              |            |            |
          |              v            v            v
          |          Qiskit/Aer    NumPy/SciPy   TOTP Library
          |              |
          |              v
          |        IBM Quantum Runtime
          |          (Optional)
          |
          v
    Visualisations
    Experiment Results
    Authentication UI
```

### Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript |
| Styling | Tailwind CSS |
| Visualisations | Recharts |
| Backend | Python, FastAPI |
| Quantum computing | IBM Qiskit |
| Local simulation | Qiskit Aer |
| Quantum hardware | IBM Quantum Runtime, optional |
| Scientific analysis | NumPy, SciPy, pandas |
| Authentication | TOTP-compatible maintained libraries |
| QR provisioning | QR-code library |

The architecture is designed to support local experimentation without requiring IBM Quantum credentials. Physical quantum hardware integration is an optional execution path.

---

## Getting Started

### Prerequisites

Install the following:

- Python 3.11 or later.
- Node.js and npm.
- Git.

Optional:

- An IBM Quantum account and appropriate credentials for physical quantum hardware experiments.

### 1. Clone the Repository

```bash
git clone https://github.com/Isomkevin/QubitKey.git
cd QubitKey
```

### 2. Backend Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS and Linux:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

The API should be accessible at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local development URL printed by Vite, typically:

```text
http://localhost:5173
```

**Note:** These commands assume the repository uses the documented `backend/` and `frontend/` layout. Refer to the actual project structure and configuration files if the implementation differs.

---

## API Overview

The backend is designed around the following API responsibilities.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Backend health check |
| `/api/config` | GET | Available execution backends and configuration |
| `/api/qrng/run` | POST | Execute a quantum randomness experiment |
| `/api/analysis/compare` | POST | Compare randomness datasets |
| `/api/experiments/{experiment_id}` | GET | Retrieve experiment metadata and results |
| `/api/experiments/{experiment_id}/export` | GET | Export experiment results |
| `/api/auth/totp/enroll` | POST | Create an authenticator enrollment |
| `/api/auth/totp/verify` | POST | Verify a time-based one-time password |

The precise request and response schemas should be documented in the backend's OpenAPI specification.

---

## IBM Quantum Hardware Integration

QubitKey is designed to support execution on physical IBM Quantum hardware through IBM Quantum Runtime.

This allows experiments to move beyond local simulation and execute quantum circuits on available quantum processors.

The distinction between execution environments is fundamental:

| Execution environment | What it demonstrates |
|---|---|
| Qiskit Aer | Classical simulation of quantum circuits |
| IBM Quantum QPU | Measurement outcomes from physical quantum hardware |

Hardware execution may involve queue times, device noise, calibration differences, shot limits, and backend availability.

QubitKey should always identify the execution backend associated with an experiment. It must never silently substitute a simulator when physical hardware execution fails.

---

## Security and Scientific Integrity

QubitKey is an experimental and educational platform. It is not presented as a certified cryptographic entropy source or a production-ready authentication service.

We maintain the following distinctions:

**Quantum randomness is not automatically cryptographic security.**

A quantum measurement experiment can generate probabilistic outcomes, but a production entropy source requires appropriate characterisation, entropy estimation, conditioning, and security engineering.

**Simulation is not physical quantum randomness.**

Qiskit Aer simulates quantum circuit behaviour on classical computing infrastructure. It is valuable for experimentation and verification, but its outputs should not be represented as physical quantum entropy.

**TOTP is not post-quantum authentication.**

TOTP is an established one-time password mechanism. Its use does not make an authentication system resistant to quantum attacks.

**QRNG is not post-quantum cryptography.**

Quantum random number generation and post-quantum cryptographic algorithms address different security requirements.

**Statistical tests are not security proofs.**

A dataset can pass statistical tests and still be unsuitable for cryptographic applications.

### Security Principles

- Use Python `secrets` for security-sensitive secret generation in the authenticator.
- Never use Python's `random` module for cryptographic secrets.
- Do not feed uncharacterised simulator output into production cryptographic operations.
- Use maintained cryptographic libraries and established standards.
- Avoid exposing authentication secrets in browser storage, logs, or API responses.
- Apply appropriate rate limits to authentication verification.
- Do not claim NIST entropy certification without the required evaluation and evidence.

---

## Project Structure

The intended project organisation is:

```text
QubitKey/
│
├── backend/
│   ├── api/
│   ├── quantum/
│   ├── analysis/
│   ├── authentication/
│   ├── services/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── charts/
│   └── package.json
│
├── notebooks/
│   └── qrng_experiments.ipynb
│
├── docs/
│   ├── PRODUCT_SPEC.md
│   ├── ARCHITECTURE.md
│   └── METHODOLOGY.md
│
├── tests/
│
├── AGENTS.md
├── README.md
├── LICENSE
└── .gitignore
```

The final repository structure may evolve as implementation progresses.

---

## Roadmap

### Phase 1: Quantum Experimentation

- [x] Define the Qiskit-based QRNG concept.
- [x] Establish the quantum measurement methodology.
- [ ] Implement configurable quantum circuit execution.
- [ ] Support repeated measurements.
- [ ] Add experiment export.

### Phase 2: Entropy Observatory

- [ ] Implement statistical analysis.
- [ ] Add interactive distribution visualisations.
- [ ] Compare quantum and classical randomness sources.
- [ ] Document experimental limitations.

### Phase 3: Digital Authentication

- [ ] Implement TOTP enrollment.
- [ ] Generate provisioning QR codes.
- [ ] Implement code verification.
- [ ] Add authentication security controls.

### Phase 4: Hardware Integration

- [ ] Integrate IBM Quantum Runtime.
- [ ] Support physical QPU execution.
- [ ] Record backend metadata and experiment provenance.
- [ ] Compare simulator and hardware measurements.

### Phase 5: Post-Quantum Exploration

- [ ] Evaluate a maintained ML-DSA implementation.
- [ ] Build an isolated signature demonstration.
- [ ] Document key generation, signing, and verification.
- [ ] Explain the relationship between quantum computing and post-quantum cryptography.

---

## Hackathon Context

**Event:** AstraCode Qiskit Fall Fest 2026  
**Project:** QubitKey  
**Tagline:** Quantum Entropy. Stronger Digital Identity.

QubitKey was developed as an exploration of how quantum computing can be translated into practical, accessible security experimentation.

Our objective is to make quantum entropy understandable, measurable, and connected to real-world digital identity challenges.

---

## Contributing

Contributions, technical feedback, research insights, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add or update relevant tests.
5. Submit a pull request with a clear explanation of the changes.

For substantial changes, open an issue first to discuss the proposed approach.

Please prioritise scientific accuracy, security, reproducibility, and maintainability.

---

## License

QubitKey is intended to be released under the MIT License.

See the `LICENSE` file for the applicable terms.

---

## Acknowledgements

- [IBM Quantum](https://quantum.ibm.com/) for quantum computing infrastructure and resources.
- [Qiskit](https://www.ibm.com/quantum/qiskit) for the open-source quantum computing framework.
- The AstraCode Qiskit Fall Fest 2026 community.

---

**QubitKey**

*Quantum Entropy. Stronger Digital Identity.*

[GitHub Repository](https://github.com/Isomkevin/QubitKey)

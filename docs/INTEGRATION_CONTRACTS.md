# QubitKey Integration Contracts

Frozen frontend/backend contracts for parallel agent work. Schema ownership: Coordinator (`backend/app/schemas/`). Changes require an ADR in `DECISIONS.md`.

Base URL (dev): `http://localhost:8000`

CORS: allow local Vite origin (`http://localhost:5173`) in development.

---

## Enumerations

### `SourceType`

```text
qiskit_simulator | ibm_qpu | python_prng | python_csprng
```

### Provenance statements (mandatory)

| Source | Statement |
|---|---|
| `qiskit_simulator` | Educational Qiskit/Aer simulation. Not physical quantum entropy. |
| `ibm_qpu` | Physical IBM Quantum measurement outcomes. Not a certified production entropy source. |
| `python_prng` | Educational Python `random.Random` PRNG. Not suitable for cryptography. |
| `python_csprng` | Operating-system CSPRNG via Python `secrets`. Classical cryptographic baseline. |

---

## Resource limits

| Parameter | Min | Max | Default |
|---|---|---|---|
| `qubits` | 1 | 8 | 8 |
| `shots` | 1 | 8192 | 1024 |
| Compare sample bits | 8 | 100000 | 4096 |
| Preview `bit_samples` / `integer_samples` | — | 256 | — |
| TOTP store TTL | — | 30 minutes | 30 minutes |
| TOTP `valid_window` | — | 1 | 1 |
| TOTP verify rate limit | — | 10 / minute / enrollment_id | — |

Exceeding validated bounds → HTTP `422`.

---

## Endpoints

### `GET /api/health`

**Response `200`**

```json
{
  "status": "ok",
  "service": "qubitkey",
  "time": "2026-11-13T00:00:00Z"
}
```

### `GET /api/config`

**Response `200`**

```json
{
  "limits": {
    "min_qubits": 1,
    "max_qubits": 8,
    "min_shots": 1,
    "max_shots": 8192,
    "max_compare_bits": 100000,
    "preview_sample_limit": 256
  },
  "sources": {
    "qiskit_simulator": { "available": true, "label": "Qiskit Aer simulator", "educational": true },
    "ibm_qpu": { "available": false, "label": "IBM Quantum hardware", "reason": "Credentials or backend not configured" },
    "python_prng": { "available": true, "label": "Python random.Random", "educational": true },
    "python_csprng": { "available": true, "label": "Python secrets CSPRNG", "educational": false }
  },
  "features": {
    "totp": true,
    "pqc": false,
    "analysis": true
  },
  "disclaimers": [
    "Simulator output is not physical quantum entropy.",
    "TOTP is not quantum-resistant.",
    "Statistical tests do not prove cryptographic security."
  ],
  "software_versions": {
    "qiskit": "2.6.2",
    "qiskit_aer": "0.18.2"
  }
}
```

### `POST /api/qrng/run`

**Request**

```json
{
  "source_type": "qiskit_simulator",
  "qubits": 8,
  "shots": 1024,
  "seed": null,
  "backend_name": null
}
```

Notes:
- `seed` allowed only for `qiskit_simulator` and `python_prng` (educational reproducibility). Never for `python_csprng` or production secret paths.
- `backend_name` optional for `ibm_qpu`; ignored otherwise.
- `ibm_qpu` when unavailable → `503` with clear error; **no simulator fallback**.

**Response `200` — `ExperimentResult`**

```json
{
  "experiment_id": "uuid",
  "source_type": "qiskit_simulator",
  "backend_name": "aer_simulator",
  "job_id": null,
  "shots": 1024,
  "qubits": 8,
  "raw_counts": { "00000000": 4, "10110101": 5 },
  "bit_samples": ["10110101"],
  "integer_samples": [181],
  "created_at": "2026-11-13T00:00:00Z",
  "software_versions": { "qiskit": "2.6.2", "qiskit_aer": "0.18.2" },
  "warnings": [],
  "provenance_statement": "Educational Qiskit/Aer simulation. Not physical quantum entropy.",
  "circuit": {
    "num_qubits": 8,
    "gates": [{ "name": "h", "qubits": [0] }],
    "measurements": true,
    "drawing": "optional text diagram"
  },
  "bit_order": "little_endian_qubit0_rightmost"
}
```

### `GET /api/experiments/{experiment_id}`

**Response `200`:** `ExperimentResult` (preview-bounded samples).  
**Response `404`:** unknown id.

### `GET /api/experiments/{experiment_id}/export`

**Response `200`:** full JSON export (may include fuller sample arrays within store retention).  
Header: `Content-Disposition: attachment; filename="qubitkey-{id}.json"`.

### `POST /api/analysis/compare`

**Request**

```json
{
  "sample_bits": 4096,
  "qubits": 8,
  "sources": ["qiskit_simulator", "python_prng", "python_csprng"],
  "seed": 42
}
```

Notes:
- All sources must produce equal bit counts.
- `ibm_qpu` included only when available; otherwise omit or return `503` for that source without substituting simulator data labelled as QPU.
- `seed` applies only to educational PRNG/simulator paths.

**Response `200`**

```json
{
  "sample_bits": 4096,
  "sources": [
    {
      "source_type": "qiskit_simulator",
      "provenance_statement": "Educational Qiskit/Aer simulation. Not physical quantum entropy.",
      "metrics": {
        "bit_count": 4096,
        "zeros": 2040,
        "ones": 2056,
        "frequency_ones": 0.502,
        "deviation_from_half": 0.002,
        "empirical_shannon_entropy_bits": 0.999,
        "longest_run": 12,
        "run_length_summary": { "mean": 2.0, "max": 12 },
        "lag1_autocorrelation": 0.01,
        "autocorrelation": { "1": 0.01, "2": -0.02 },
        "integer_histogram": { "0": 10, "255": 8 },
        "chi_square": {
          "stat": 1.2,
          "p_value": 0.27,
          "applicable": true,
          "limitation": "Educational diagnostic only; not cryptographic certification."
        }
      }
    }
  ],
  "caveats": [
    "Passing these diagnostics does not prove cryptographic security or sufficient min-entropy.",
    "Equal sample sizes are used for fairness; do not over-interpret single runs."
  ],
  "created_at": "2026-11-13T00:00:00Z"
}
```

### `POST /api/auth/totp/enroll`

**Request**

```json
{
  "account_label": "demo@local",
  "issuer": "QubitKey"
}
```

**Response `200`**

```json
{
  "enrollment_id": "uuid",
  "account_label": "demo@local",
  "issuer": "QubitKey",
  "secret_base32": "…",
  "otpauth_uri": "otpauth://totp/…",
  "qr_png_base64": "…",
  "expires_at": "2026-11-13T00:30:00Z",
  "warnings": [
    "Keep this secret private. Do not share or commit it.",
    "TOTP is not quantum-resistant. Secret was generated with OS CSPRNG.",
    "Demo store is in-memory and short-lived; not production security."
  ]
}
```

Headers: `Cache-Control: no-store`

### `POST /api/auth/totp/verify`

**Request**

```json
{
  "enrollment_id": "uuid",
  "otp": "123456"
}
```

**Response `200`**

```json
{ "valid": true }
```

or `{ "valid": false }` for invalid/expired/unknown (avoid detailed attacker hints).  
Rate limited → `429`.

### Optional PQC (Milestone 6)

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/pqc/keygen` | Generate ML-DSA-65 key pair; return public key + session id; secret key held in short-lived memory |
| POST | `/api/pqc/challenge` | Fresh OS-CSPRNG challenge for session |
| POST | `/api/pqc/verify` | Verify signature over challenge; reject replays |

UI and responses must state: ML-DSA is a post-quantum signature scheme; separate from QRNG and TOTP.

---

## Bit ordering contract

- Qiskit measurement bitstrings use **little-endian display**: qubit 0 is the **rightmost** character.
- Integer conversion: interpret the bitstring as binary with that endianness consistently.
- Every experiment response includes `"bit_order": "little_endian_qubit0_rightmost"`.
- Unit tests lock this behaviour.

## Circuit diagram payload

Frontend must render from `circuit` data returned by the API (gates list and/or text drawing). Decorative fake circuits are not acceptable as experimental representation.

## Error shape

```json
{
  "detail": "Human-readable error message"
}
```

Use FastAPI/HTTPException conventions. Never include secrets, OTPs, or provisioning URIs in error bodies or logs.

## Frontend client rules

- Single API client module; no cryptographic logic in the browser beyond displaying provisioning material once.
- Never persist TOTP secrets, OTPs, or otpauth URIs in `localStorage` / `sessionStorage`.
- Charts must cite `source_type` and sample size.
- Loading, error, and empty states required on all data views.

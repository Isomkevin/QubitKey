# Experiment Methodology

Educational methodology for QubitKey QRNG experiments. Interactive runs: [https://qubitkey.vercel.app](https://qubitkey.vercel.app). API contracts: [`INTEGRATION_CONTRACTS.md`](INTEGRATION_CONTRACTS.md).

## Circuit

1. Initialise `n` qubits in `|0⟩`.
2. Apply Hadamard `H` to each qubit.
3. Measure all qubits (`measure_all`, classical register `meas`).
4. Collect `shots` samples.

Ideal single-qubit measurement yields 0 or 1 with probability 1/2 each.

## Bit ordering

Qiskit bitstrings are interpreted as **little-endian with qubit 0 rightmost**. Integer conversion uses that convention consistently (`bit_order: little_endian_qubit0_rightmost`).

## Sources

| Source | Meaning |
|---|---|
| `qiskit_simulator` | Aer `SamplerV2` — educational simulation |
| `ibm_qpu` | IBM Quantum Runtime Sampler — physical measurements when configured |
| `python_prng` | `random.Random` — educational PRNG |
| `python_csprng` | `secrets` — OS CSPRNG baseline |

Comparisons use equal bit counts. Seeds apply only to educational simulator/PRNG paths.

## Metrics (educational)

- Zero/one frequency and deviation from 0.5
- Integer histogram
- Longest run and run-length summary
- Empirical Shannon entropy (binary alphabet)
- Lagged autocorrelation
- Chi-square vs fair coin when expected counts allow

### Limitations

These diagnostics can detect some biases. They **do not**:

- prove cryptographic unpredictability,
- estimate NIST SP 800-90B min-entropy,
- certify an entropy source for production key generation.

## Rejection sampling

For non-power-of-two ranges (e.g. fair die), discard out-of-range values rather than taking modulo.

## Reproducibility

Record `qubits`, `shots`, `source_type`, `backend_name`, `job_id` (if any), timestamps, software versions, warnings, and provenance statement with every export.

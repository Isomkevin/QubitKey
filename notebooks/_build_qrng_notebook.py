"""Generate notebooks/qrng_experiments.ipynb (stdlib only)."""

from __future__ import annotations

import json
from pathlib import Path


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip("\n").splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip("\n").splitlines(keepends=True),
    }


cells: list[dict] = []

cells.append(
    md(
        """
# QubitKey QRNG Research Notebook

**Quantum Entropy Laboratory — educational Hadamard measurement experiments with Qiskit**

This notebook is a standalone research and teaching artefact for QubitKey. It builds real Qiskit circuits, executes them locally with **Qiskit Aer**, compares outcomes against Python `random` and `secrets`, and analyses the resulting samples with transparent statistical diagnostics.

## Research objective

Investigate how a Hadamard-based quantum circuit produces measurement bitstrings that can be treated as *candidate* random samples for **educational** study — and to contrast that behaviour with classical pseudorandom (PRNG) and OS-backed cryptographically secure (CSPRNG) generators.

## What this notebook claims — and what it does not

| Claim | Status |
|---|---|
| Aer simulates Hadamard measurement statistics | Yes |
| Equal-size comparison across Aer / `random` / `secrets` | Yes |
| Empirical statistics (frequency, entropy, runs, autocorrelation, chi-square) | Yes |
| Aer output is **physical quantum entropy** | **No** |
| Passing statistical tests proves cryptographic security | **No** |
| QRNG is post-quantum cryptography | **No** |
| TOTP is quantum-resistant | **No** |
| NIST SP 800-90B / entropy certification | **Not performed** |

## Distinguishing related concepts

- **PRNG** (`random.Random`): deterministic algorithm; seedable; educational only for security.
- **OS CSPRNG** (`secrets`): operating-system entropy interface; appropriate for secrets in software demos.
- **QRNG (this experiment)**: measurement outcomes from a quantum circuit model (simulator) or, optionally, physical hardware.
- **Post-quantum cryptography (PQC)**: algorithms (e.g. ML-DSA) designed to resist quantum *attacks* on crypto — a different problem from randomness generation.

> **Mandatory honesty:** Qiskit Aer runs on classical hardware. Its bitstrings are **simulated**, not physical quantum entropy. Optional IBM Quantum cells require explicit configuration and never silently fall back to the simulator.
"""
    )
)

cells.append(
    md(
        """
## 1. Environment verification

Install dependencies from `notebooks/requirements.txt`, then run this notebook top-to-bottom. The helper module `qrng_lab.py` lives beside this notebook.
"""
    )
)

cells.append(
    code(
        """
from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import qiskit
import qiskit_aer
from IPython.display import display
from qiskit.visualization import plot_histogram

# Ensure the notebooks/ directory is importable when the kernel cwd differs.
NOTEBOOK_DIR = Path.cwd()
if not (NOTEBOOK_DIR / "qrng_lab.py").exists():
    candidate = Path.cwd() / "notebooks"
    if (candidate / "qrng_lab.py").exists():
        NOTEBOOK_DIR = candidate
        sys.path.insert(0, str(NOTEBOOK_DIR))
    else:
        sys.path.insert(0, str(Path.cwd()))
else:
    sys.path.insert(0, str(NOTEBOOK_DIR))

import qrng_lab as lab

print("Python:", sys.version.split()[0])
print("Working directory:", Path.cwd())
print("qrng_lab:", lab.__file__)
for name, version in lab.software_versions().items():
    print(f"{name}: {version}")

%matplotlib inline
plt.rcParams["figure.figsize"] = (9, 4)
plt.rcParams["axes.grid"] = True
"""
    )
)

cells.append(
    md(
        """
### Experiment configuration

Adjust qubits, shots, and seed below. Inputs are validated against notebook limits (`MAX_QUBITS`, `MAX_SHOTS`) to keep local runs tractable.
"""
    )
)

cells.append(
    code(
        """
N_QUBITS = lab.DEFAULT_QUBITS  # 8 -> integers in 0..255
SHOTS = lab.DEFAULT_SHOTS      # equal sample size for comparisons
SEED = lab.DEFAULT_SEED        # Aer + PRNG reproducibility only; never seed secrets
RUN_IBM_HARDWARE = False       # Explicit opt-in for physical IBM Quantum execution

lab.validate_experiment(N_QUBITS, SHOTS)
print(f"N_QUBITS={N_QUBITS}, SHOTS={SHOTS}, SEED={SEED}")
print(f"RUN_IBM_HARDWARE={RUN_IBM_HARDWARE}")
print(f"Limits: MAX_QUBITS={lab.MAX_QUBITS}, MAX_SHOTS={lab.MAX_SHOTS}")
print(lab.SIMULATOR_WARNING)
"""
    )
)

cells.append(
    md(
        r"""
## 2. Quantum circuit construction

For each qubit initialised in $|0\rangle$, a Hadamard gate prepares an equal superposition:

$$
H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

Independent Hadamards on $n$ qubits, followed by computational-basis measurement, yield an $n$-bit string per shot. Ideal independent fair bits imply each of the $2^n$ outcomes appears with probability $2^{-n}$.
"""
    )
)

cells.append(
    code(
        """
qc = lab.build_hadamard_qrng(N_QUBITS)
print(qc.draw(output="text"))
try:
    display(qc.draw(output="mpl"))
except Exception as exc:  # noqa: BLE001
    print("Matplotlib circuit drawer unavailable:", exc)
"""
    )
)

cells.append(
    md(
        """
## 3. Hadamard superposition — small demonstration

A single-qubit Hadamard circuit with modest shots should produce roughly balanced `0`/`1` counts under Aer. Balance here illustrates the *modelled* measurement statistics; it is not a cryptographic proof.
"""
    )
)

cells.append(
    code(
        """
demo = lab.run_aer_qrng(n_qubits=1, shots=512, seed=SEED)
print("Provenance:", demo["provenance"]["provenance_statement"])
print("Counts:", demo["counts"])
fig = plot_histogram(demo["counts"], title="1-qubit Hadamard (Aer, 512 shots)")
display(fig)
plt.close("all")
"""
    )
)

cells.append(
    md(
        """
## 4. Measurement and execution with Qiskit Aer

We execute the full $n$-qubit circuit using Aer `SamplerV2` with an explicit simulator seed. The provenance record labels the source as `qiskit_simulator`.
"""
    )
)

cells.append(
    code(
        """
aer_result = lab.run_aer_qrng(qc=qc, n_qubits=N_QUBITS, shots=SHOTS, seed=SEED)
aer_counts = aer_result["counts"]
aer_bitstrings = aer_result["bitstrings"]
aer_integers = aer_result["integers"]
aer_bits = aer_result["bits"]
aer_prov = aer_result["provenance"]

print("source_type:", aer_prov["source_type"])
print("backend_name:", aer_prov["backend_name"])
print("shots / qubits:", aer_prov["shots"], "/", aer_prov["qubits"])
print("seed:", aer_prov["seed"])
print("warnings:")
for w in aer_prov["warnings"]:
    print(" -", w)
print("Distinct outcomes observed:", len(aer_counts), "of", 2**N_QUBITS)
print("First 8 bitstrings:", aer_bitstrings[:8])
print("First 8 integers:", aer_integers[:8])
"""
    )
)

cells.append(
    md(
        """
## 5. Binary-to-integer conversion and Qiskit bit ordering

Qiskit displays classical bitstrings in **little-endian** form: **qubit 0 is the rightmost character (LSB)**.

| Bitstring | Qubit 1 | Qubit 0 | Integer |
|---|---|---|---|
| `00` | 0 | 0 | 0 |
| `01` | 0 | 1 | 1 |
| `10` | 1 | 0 | 2 |
| `11` | 1 | 1 | 3 |

Conversion uses `int(bitstring, 2)`, which matches that convention when the string is Qiskit's display order.
"""
    )
)

cells.append(
    code(
        """
examples = ["00", "01", "10", "11"]
rows = []
for bs in examples:
    bits = lab.bits_lsb_first(bs)
    rows.append(
        {
            "bitstring": bs,
            "q0 (LSB)": bits[0],
            "q1": bits[1],
            "integer": lab.bitstring_to_int(bs),
        }
    )
display(pd.DataFrame(rows))

assert lab.bitstring_to_int("01") == 1
assert lab.bitstring_to_int("10") == 2
assert aer_integers == [lab.bitstring_to_int(bs) for bs in aer_bitstrings]
print("Conversion checks passed for Aer samples.")
"""
    )
)

cells.append(
    md(
        """
### Avoiding modulo bias for bounded integers

Mapping raw bits to a range whose size is not a power of two via `n % bound` biases the distribution. Rejection sampling draws from the next power-of-two range and **discards** illegal outcomes. For a fair die (`bound=6`), three bits yield `{0..7}`; outcomes `6` and `7` are rejected.
"""
    )
)

cells.append(
    code(
        """
# Generate enough 3-qubit shots so rejection sampling can produce many d6 rolls.
die_run = lab.run_aer_qrng(n_qubits=3, shots=2048, seed=SEED)
try:
    rolls = lab.rejection_sample_many(die_run["bitstrings"], bound=6, count=500)
except RuntimeError as exc:
    raise RuntimeError("Increase shots for the die demo if rejection exhausts bits.") from exc

roll_counts = pd.Series(rolls).value_counts().sort_index()
display(roll_counts.to_frame("count"))
fig, ax = plt.subplots()
ax.bar(roll_counts.index.astype(str), roll_counts.values, color="#2a6f97")
ax.set_title("Fair d6 via rejection sampling (Aer bits; educational)")
ax.set_xlabel("Face (0..5)")
ax.set_ylabel("Count")
plt.tight_layout()
plt.show()
print("Empirical frequencies:", (roll_counts / roll_counts.sum()).to_dict())
"""
    )
)

cells.append(
    md(
        """
## 6. Repeated quantum measurement experiments

The primary Aer dataset uses the configured `SHOTS` and `N_QUBITS`. Ideal theory predicts a flat histogram over $2^{n}$ bins; finite samples fluctuate.
"""
    )
)

cells.append(
    code(
        """
print(f"Primary Aer dataset: {len(aer_integers)} integers in 0..{2**N_QUBITS - 1}")
top = sorted(aer_counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
print("Top 10 bitstring counts:")
for bs, c in top:
    print(f"  {bs}: {c}")

fig = plot_histogram(
    dict(top),
    title=f"Top outcomes (Aer, n={N_QUBITS}, shots={SHOTS})",
)
display(fig)
plt.close("all")
"""
    )
)

cells.append(
    md(
        """
## 7. Comparison against Python `random` and `secrets`

All three sources produce **equal** sample counts of $n$-bit integers:

1. **Aer Hadamard QRNG (simulated)** — educational quantum circuit model.
2. **`random.Random(SEED)`** — deterministic PRNG (seeded for reproducibility).
3. **`secrets`** — OS-backed CSPRNG (not seeded).

Equal $N$ avoids unfair visual or statistical comparisons caused by mismatched sample sizes.
"""
    )
)

cells.append(
    code(
        """
comparison = lab.compare_sources(n_samples=SHOTS, n_bits=N_QUBITS, seed=SEED)

# Reuse the seeded Aer result already computed for provenance continuity.
comparison["aer"] = aer_result
comparison["aer"]["bits"] = aer_bits

prng_integers = comparison["prng_integers"]
csprng_integers = comparison["csprng_integers"]
prng_bits = comparison["prng_bits"]
csprng_bits = comparison["csprng_bits"]

assert len(aer_integers) == len(prng_integers) == len(csprng_integers) == SHOTS

summary_rows = [
    lab.summarize_bit_source("qiskit_aer_sim", aer_bits, aer_integers, N_QUBITS),
    lab.summarize_bit_source("python_prng", prng_bits, prng_integers, N_QUBITS),
    lab.summarize_bit_source("python_csprng", csprng_bits, csprng_integers, N_QUBITS),
]
summary_df = pd.DataFrame(summary_rows)
display(summary_df)
"""
    )
)

cells.append(
    md(
        """
## 8. Statistical analysis and visualisations

Metrics below are computed from **this run's** arrays. They are diagnostic and educational.

**Important limitations**

- Empirical Shannon entropy is a plug-in estimate on the observed distribution — **not** cryptographic min-entropy and **not** NIST SP 800-90B.
- Chi-square tests assume adequate expected counts; low expected counts weaken the approximation.
- Passing these tests does **not** establish cryptographic security.
"""
    )
)

cells.append(
    code(
        """
sources = {
    "Aer (sim)": (aer_bits, aer_integers),
    "random.Random": (prng_bits, prng_integers),
    "secrets": (csprng_bits, csprng_integers),
}

# Bit frequency
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=True)
for ax, (name, (bits, _)) in zip(axes, sources.items()):
    freq = lab.bit_frequency(bits)
    ax.bar(["0", "1"], [freq["p0"], freq["p1"]], color=["#014f86", "#61a5c2"])
    ax.set_ylim(0, 1)
    ax.set_title(name)
    ax.set_xlabel("Bit value")
axes[0].set_ylabel("Empirical frequency")
fig.suptitle("Bit frequency by source")
plt.tight_layout()
plt.show()
"""
    )
)

cells.append(
    code(
        """
# Integer histograms
fig, axes = plt.subplots(1, 3, figsize=(14, 3.8), sharey=True)
bins = np.arange(0, 2**N_QUBITS + 1)
for ax, (name, (_, ints)) in zip(axes, sources.items()):
    ax.hist(ints, bins=bins, color="#2a6f97", alpha=0.9)
    ax.set_title(name)
    ax.set_xlabel("Integer value")
axes[0].set_ylabel("Count")
fig.suptitle(f"Integer histograms (n_bits={N_QUBITS}, N={SHOTS})")
plt.tight_layout()
plt.show()
"""
    )
)

cells.append(
    code(
        """
# Empirical entropy, longest runs, autocorrelation, chi-square
stat_rows = []
auto_by_source = {}
for name, (bits, ints) in sources.items():
    freq = lab.bit_frequency(bits)
    runs = lab.longest_run(bits)
    auto = lab.autocorrelation(bits, max_lag=20)
    auto_by_source[name] = auto
    bit_chi = lab.chi_square_bit_balance(bits)
    int_chi = lab.chi_square_uniform_integers(ints, n_bins=2**N_QUBITS)
    stat_rows.append(
        {
            "source": name,
            "p1": freq["p1"],
            "H_bits_empirical": lab.empirical_shannon_entropy(list(bits)),
            "H_ints_empirical": lab.empirical_shannon_entropy(list(ints)),
            "H_ints_max": float(N_QUBITS),
            "longest_0": runs["longest_0"],
            "longest_1": runs["longest_1"],
            "lag1_acf": auto["lag1"],
            "chi2_bit_p": bit_chi["p_value"],
            "chi2_int_p": int_chi["p_value"],
            "chi2_int_low_expected": int_chi["low_expected_counts"],
        }
    )

stats_df = pd.DataFrame(stat_rows)
display(stats_df)

print("Chi-square caveats:")
print(" -", lab.chi_square_bit_balance(aer_bits)["caveat"])
print(" -", lab.chi_square_uniform_integers(aer_integers, 2**N_QUBITS)["caveat"])
"""
    )
)

cells.append(
    code(
        """
fig, ax = plt.subplots(figsize=(9, 4))
for name, auto in auto_by_source.items():
    ax.plot(auto["lags"], auto["autocorrelation"], marker="o", label=name)
ax.axhline(0.0, color="black", linewidth=0.8)
ax.set_xlabel("Lag")
ax.set_ylabel("Autocorrelation")
ax.set_title("Bit-stream autocorrelation (educational diagnostic)")
ax.legend()
plt.tight_layout()
plt.show()
"""
    )
)

cells.append(
    md(
        """
## 9. Interpretation of findings and scientific limitations

Interpret the tables and plots above as **this execution's** empirical behaviour under the chosen seed, shot count, and qubit width.

### Expected qualitative behaviour (Aer ideal model)

- Bit frequencies near 1/2.
- Integer histogram without gross structure at large N.
- Empirical bit entropy near 1 bit/symbol; integer entropy approaching n bits for well-spread samples.
- Autocorrelation near 0 at small lags for independent ideal bits.

Finite-sample fluctuations are normal. A “nice looking” histogram is **not** certification.

### Scientific limitations (read carefully)

1. **Simulator is not a physical QRNG.** Aer classically samples the circuit probability distribution (up to numerical/RNG details of the simulator).
2. **Hardware needs provenance.** Physical claims require a real IBM backend job ID and metadata (optional section below).
3. **Statistics are not security.** Frequency, entropy, runs, autocorrelation, and chi-square can miss structured weaknesses relevant to cryptography.
4. **No NIST 90B.** This notebook does not estimate min-entropy for entropy-source validation.
5. **QRNG is not PQC.** Randomness generation does not provide quantum-resistant signatures or KEMs.
6. **Do not feed uncharacterised simulator bits into production key generation.** Use `secrets` (or a characterised entropy architecture) for security-sensitive secrets.

Any numerical values in outputs are from live execution of the cells above — not invented illustrative figures pasted into markdown.
"""
    )
)

cells.append(
    md(
        """
## 10. Optional IBM Quantum physical hardware execution

This section is **opt-in**. Default `RUN_IBM_HARDWARE = False` skips hardware so the notebook runs without credentials.

When enabled:

- Requires `IBM_QUANTUM_TOKEN` (and recommended `IBM_QUANTUM_INSTANCE`).
- Uses current IBM Quantum Runtime interfaces (`QiskitRuntimeService` + `Sampler`).
- Refuses simulator backends.
- **Never** falls back to Aer on failure.
"""
    )
)

cells.append(
    code(
        """
ibm_hardware_result = None

if not RUN_IBM_HARDWARE:
    print("RUN_IBM_HARDWARE is False — skipping physical IBM Quantum execution.")
    print("No hardware results are fabricated. Set RUN_IBM_HARDWARE=True and provide credentials to run on a QPU.")
else:
    token = os.environ.get("IBM_QUANTUM_TOKEN") or os.environ.get("QISKIT_IBM_TOKEN")
    instance = os.environ.get("IBM_QUANTUM_INSTANCE")
    if not token:
        raise RuntimeError(
            "IBM Quantum credentials required for hardware mode. "
            "Set IBM_QUANTUM_TOKEN (and ideally IBM_QUANTUM_INSTANCE). "
            "Refusing to fall back to the Aer simulator."
        )

    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

    service_kwargs = {
        "channel": "ibm_quantum_platform",
        "token": token,
    }
    if instance:
        service_kwargs["instance"] = instance

    service = QiskitRuntimeService(**service_kwargs)
    backend = service.least_busy(operational=True, simulator=False)
    lab.assert_non_simulator_backend(backend)

    # Keep hardware shots modest unless the user raises them deliberately.
    hardware_shots = min(SHOTS, 1024)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_qc = pm.run(lab.build_hadamard_qrng(min(N_QUBITS, 8)))

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_qc], shots=hardware_shots)
    result = job.result()
    pub = result[0]
    # Prefer classical register "c"; measure_all-style "meas" as fallback.
    data = pub.data
    bit_array = getattr(data, "c", None) or getattr(data, "meas", None)
    if bit_array is None:
        raise RuntimeError("Hardware result did not expose expected classical data fields.")

    hw_bitstrings = list(bit_array.get_bitstrings())
    hw_counts = dict(bit_array.get_counts())
    hw_integers = [lab.bitstring_to_int(bs) for bs in hw_bitstrings]

    ibm_hardware_result = {
        "source_type": "ibm_qpu",
        "backend_name": backend.name,
        "job_id": job.job_id(),
        "shots": hardware_shots,
        "qubits": isa_qc.num_qubits,
        "counts": hw_counts,
        "bitstrings": hw_bitstrings,
        "integers": hw_integers,
        "simulator": False,
        "created_at": lab.Provenance(
            source_type="ibm_qpu",
            backend_name=backend.name,
            shots=hardware_shots,
            qubits=isa_qc.num_qubits,
            job_id=job.job_id(),
            software_versions=lab.software_versions(),
            provenance_statement=(
                "Physical IBM Quantum execution. Outcomes are hardware measurements, "
                "but are not certified as a production entropy source without further evaluation."
            ),
        ).as_dict(),
    }
    print("IBM Quantum hardware run complete.")
    print("backend:", ibm_hardware_result["backend_name"])
    print("job_id:", ibm_hardware_result["job_id"])
    print("shots:", ibm_hardware_result["shots"])
    print("distinct outcomes:", len(hw_counts))
"""
    )
)

cells.append(
    md(
        """
## 11. Reproducibility and provenance summary

Re-run all cells after changing seeds or shot counts. PRNG comparisons intentionally reuse `SEED`; `secrets` does not. Hardware runs add backend name and job ID when enabled.
"""
    )
)

cells.append(
    code(
        """
provenance_report = {
    "experiment": "QubitKey Hadamard QRNG notebook",
    "config": {
        "N_QUBITS": N_QUBITS,
        "SHOTS": SHOTS,
        "SEED": SEED,
        "RUN_IBM_HARDWARE": RUN_IBM_HARDWARE,
    },
    "aer_provenance": aer_prov,
    "comparison_sources": ["qiskit_simulator", "python_prng", "python_csprng"],
    "ibm_hardware_provenance": None
    if ibm_hardware_result is None
    else ibm_hardware_result["created_at"],
    "scientific_limitations": [
        "Aer output is simulated, not physical quantum entropy.",
        "Statistical tests do not prove cryptographic security.",
        "QRNG is not post-quantum cryptography.",
        "No NIST SP 800-90B evaluation was performed.",
    ],
}

display(pd.Series({k: str(v) for k, v in provenance_report.items() if k != "aer_provenance"}).to_frame("value"))
print("\\nAer provenance detail:")
for key, value in aer_prov.items():
    print(f"  {key}: {value}")

print("\\nNotebook execution reached the final cell successfully.")
"""
    )
)

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    },
    "cells": cells,
}

out = Path(__file__).resolve().parent / "qrng_experiments.ipynb"
out.write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"Wrote {out} with {len(cells)} cells")

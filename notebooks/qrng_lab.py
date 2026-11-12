"""QubitKey notebook helpers for Hadamard QRNG experiments.

Educational utilities only. Aer simulator output is classical simulation of
quantum circuits and must never be labelled as physical quantum entropy.
Statistical helpers do not establish cryptographic security.
"""

from __future__ import annotations

import math
import random
import secrets
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import islice
from typing import Any, Iterable, Iterator, Sequence

import numpy as np
from scipy import stats

try:
    import qiskit
    from qiskit import QuantumCircuit
    from qiskit_aer.primitives import SamplerV2 as AerSampler
except ImportError as exc:  # pragma: no cover - surfaced at notebook import time
    raise ImportError(
        "qiskit and qiskit-aer are required. Install notebooks/requirements.txt."
    ) from exc

MAX_QUBITS = 16
MAX_SHOTS = 20_000
DEFAULT_QUBITS = 8
DEFAULT_SHOTS = 4096
DEFAULT_SEED = 42

SIMULATOR_WARNING = (
    "Qiskit Aer output is a classical simulation of quantum circuit behaviour. "
    "It is not physical quantum entropy."
)


@dataclass
class Provenance:
    """Run metadata for scientific honesty and reproducibility."""

    source_type: str
    backend_name: str
    shots: int
    qubits: int
    seed: int | None = None
    job_id: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    software_versions: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    provenance_statement: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "backend_name": self.backend_name,
            "shots": self.shots,
            "qubits": self.qubits,
            "seed": self.seed,
            "job_id": self.job_id,
            "created_at": self.created_at,
            "software_versions": dict(self.software_versions),
            "warnings": list(self.warnings),
            "provenance_statement": self.provenance_statement,
        }


def software_versions() -> dict[str, str]:
    """Return versions of key scientific packages when available."""
    versions: dict[str, str] = {"qiskit": qiskit.__version__}
    try:
        import qiskit_aer

        versions["qiskit_aer"] = qiskit_aer.__version__
    except Exception:  # noqa: BLE001
        versions["qiskit_aer"] = "unknown"
    try:
        import qiskit_ibm_runtime

        versions["qiskit_ibm_runtime"] = qiskit_ibm_runtime.__version__
    except Exception:  # noqa: BLE001
        versions["qiskit_ibm_runtime"] = "not-installed"
    versions["numpy"] = np.__version__
    try:
        import scipy

        versions["scipy"] = scipy.__version__
    except Exception:  # noqa: BLE001
        versions["scipy"] = "unknown"
    return versions


def validate_experiment(
    n_qubits: int,
    shots: int,
    *,
    max_qubits: int = MAX_QUBITS,
    max_shots: int = MAX_SHOTS,
) -> None:
    """Validate experiment parameters against sensible notebook limits."""
    if not isinstance(n_qubits, int) or isinstance(n_qubits, bool):
        raise TypeError("n_qubits must be an int")
    if not isinstance(shots, int) or isinstance(shots, bool):
        raise TypeError("shots must be an int")
    if n_qubits < 1:
        raise ValueError("n_qubits must be >= 1")
    if shots < 1:
        raise ValueError("shots must be >= 1")
    if n_qubits > max_qubits:
        raise ValueError(f"n_qubits={n_qubits} exceeds MAX_QUBITS={max_qubits}")
    if shots > max_shots:
        raise ValueError(f"shots={shots} exceeds MAX_SHOTS={max_shots}")


def build_hadamard_qrng(n_qubits: int) -> QuantumCircuit:
    """Build an n-qubit Hadamard QRNG circuit with explicit measure(q_i -> c_i)."""
    validate_experiment(n_qubits, 1)
    qc = QuantumCircuit(n_qubits, n_qubits, name="hadamard_qrng")
    for q in range(n_qubits):
        qc.h(q)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def bitstring_to_int(bitstring: str) -> int:
    """Convert a Qiskit little-endian display bitstring to an integer.

    Qiskit prints qubit 0 as the rightmost character (LSB). Example:
    ``\"01\"`` means qubit0=1, qubit1=0 and converts to integer 1.
    """
    if not bitstring:
        raise ValueError("bitstring must be non-empty")
    if any(ch not in "01" for ch in bitstring):
        raise ValueError(f"bitstring must contain only 0/1 characters: {bitstring!r}")
    return int(bitstring, 2)


def bits_lsb_first(bitstring: str) -> list[int]:
    """Return ``[q0, q1, ..., q_{n-1}]`` from a Qiskit little-endian bitstring."""
    if not bitstring:
        raise ValueError("bitstring must be non-empty")
    if any(ch not in "01" for ch in bitstring):
        raise ValueError(f"bitstring must contain only 0/1 characters: {bitstring!r}")
    return [int(b) for b in reversed(bitstring)]


def flatten_bits_lsb_first(bitstrings: Sequence[str]) -> list[int]:
    """Flatten shot bitstrings into a LSB-first bit stream."""
    bits: list[int] = []
    for bs in bitstrings:
        bits.extend(bits_lsb_first(bs))
    return bits


def rejection_sample_bounded(bit_iter: Iterator[int], bound: int) -> int:
    """Draw one unbiased integer in ``{0 .. bound-1}`` via rejection sampling.

    Avoids modulo bias when ``bound`` is not a power of two. For a fair six-sided
    die, consume three bits and reject outcomes 6 and 7.
    """
    if bound <= 0:
        raise ValueError("bound must be positive")
    limit = 1
    while limit < bound:
        limit <<= 1
    nbits = limit.bit_length() - 1
    if nbits == 0:
        return 0
    while True:
        value = 0
        for _ in range(nbits):
            try:
                bit = next(bit_iter)
            except StopIteration as exc:
                raise RuntimeError(
                    "ran out of bits while rejection sampling; generate more shots"
                ) from exc
            if bit not in (0, 1):
                raise ValueError(f"bits must be 0 or 1, got {bit!r}")
            value = (value << 1) | bit
        if value < bound:
            return value


def rejection_sample_many(
    bitstrings: Sequence[str],
    bound: int,
    count: int,
) -> list[int]:
    """Produce ``count`` unbiased integers in ``{0 .. bound-1}`` from shot bits."""
    bit_iter = iter(flatten_bits_lsb_first(bitstrings))
    return [rejection_sample_bounded(bit_iter, bound) for _ in range(count)]


def _extract_bit_array(pub_result: Any):
    """Return the classical BitArray from a SamplerV2 pub result."""
    data = pub_result.data
    if hasattr(data, "c"):
        return data.c
    if hasattr(data, "meas"):
        return data.meas
    # Fall back to the first available attribute that looks like a BitArray.
    for name in dir(data):
        if name.startswith("_"):
            continue
        attr = getattr(data, name)
        if hasattr(attr, "get_bitstrings") and hasattr(attr, "get_counts"):
            return attr
    raise AttributeError("Could not locate classical BitArray on SamplerV2 result")


def run_aer_qrng(
    qc: QuantumCircuit | None = None,
    *,
    n_qubits: int = DEFAULT_QUBITS,
    shots: int = DEFAULT_SHOTS,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Execute a Hadamard QRNG circuit on Aer SamplerV2 with provenance."""
    validate_experiment(n_qubits if qc is None else qc.num_qubits, shots)
    circuit = qc if qc is not None else build_hadamard_qrng(n_qubits)
    qubits = circuit.num_qubits
    sampler = AerSampler(default_shots=shots, seed=seed)
    job = sampler.run([circuit], shots=shots)
    pub_result = job.result()[0]
    bit_array = _extract_bit_array(pub_result)
    bitstrings = list(bit_array.get_bitstrings())
    counts = dict(bit_array.get_counts())
    integers = [bitstring_to_int(bs) for bs in bitstrings]
    provenance = Provenance(
        source_type="qiskit_simulator",
        backend_name="aer_simulator",
        shots=shots,
        qubits=qubits,
        seed=seed,
        software_versions=software_versions(),
        warnings=[SIMULATOR_WARNING],
        provenance_statement=(
            "Educational Aer simulation of a Hadamard measurement circuit. "
            "Not a physical quantum entropy source."
        ),
    )
    return {
        "circuit": circuit,
        "counts": counts,
        "bitstrings": bitstrings,
        "integers": integers,
        "bits": flatten_bits_lsb_first(bitstrings),
        "provenance": provenance.as_dict(),
    }


def python_prng_integers(n_samples: int, n_bits: int, seed: int) -> list[int]:
    """Educational PRNG samples using ``random.Random`` (not for secrets)."""
    if n_samples < 1 or n_bits < 1:
        raise ValueError("n_samples and n_bits must be >= 1")
    upper = 1 << n_bits
    rng = random.Random(seed)
    return [rng.randrange(upper) for _ in range(n_samples)]


def python_csprng_integers(n_samples: int, n_bits: int) -> list[int]:
    """OS-backed CSPRNG samples using ``secrets`` (not seeded)."""
    if n_samples < 1 or n_bits < 1:
        raise ValueError("n_samples and n_bits must be >= 1")
    upper = 1 << n_bits
    return [secrets.randbelow(upper) for _ in range(n_samples)]


def integers_to_bits(integers: Sequence[int], n_bits: int) -> list[int]:
    """Expand integers into LSB-first bit lists of fixed width."""
    if n_bits < 1:
        raise ValueError("n_bits must be >= 1")
    bits: list[int] = []
    for value in integers:
        if value < 0 or value >= (1 << n_bits):
            raise ValueError(f"value {value} does not fit in {n_bits} bits")
        for i in range(n_bits):
            bits.append((value >> i) & 1)
    return bits


def compare_sources(
    *,
    n_samples: int = DEFAULT_SHOTS,
    n_bits: int = DEFAULT_QUBITS,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Generate equal-sized samples from Aer, PRNG, and CSPRNG."""
    validate_experiment(n_bits, n_samples)
    aer = run_aer_qrng(n_qubits=n_bits, shots=n_samples, seed=seed)
    prng = python_prng_integers(n_samples, n_bits, seed)
    csprng = python_csprng_integers(n_samples, n_bits)
    return {
        "n_samples": n_samples,
        "n_bits": n_bits,
        "seed": seed,
        "aer": aer,
        "prng_integers": prng,
        "csprng_integers": csprng,
        "prng_bits": integers_to_bits(prng, n_bits),
        "csprng_bits": integers_to_bits(csprng, n_bits),
    }


def bit_frequency(bits: Sequence[int]) -> dict[str, float | int]:
    """Return counts and proportions for a binary bit stream."""
    if not bits:
        raise ValueError("bits must be non-empty")
    arr = np.asarray(bits, dtype=int)
    if not np.isin(arr, [0, 1]).all():
        raise ValueError("bits must contain only 0 and 1")
    n = int(arr.size)
    ones = int(arr.sum())
    zeros = n - ones
    return {
        "n_bits": n,
        "zeros": zeros,
        "ones": ones,
        "p0": zeros / n,
        "p1": ones / n,
    }


def empirical_shannon_entropy(values: Sequence[int], *, n_symbols: int | None = None) -> float:
    """Empirical Shannon entropy in bits from observed discrete values.

    This is an empirical plug-in estimate, not a cryptographic min-entropy
    evaluation and not a NIST SP 800-90B assessment.
    """
    if not values:
        raise ValueError("values must be non-empty")
    counts = Counter(values)
    n = len(values)
    entropy = 0.0
    for count in counts.values():
        p = count / n
        if p > 0:
            entropy -= p * math.log2(p)
    if n_symbols is not None:
        # Entropy is still computed from the observed distribution only.
        _ = n_symbols
    return float(entropy)


def longest_run(bits: Sequence[int], symbol: int | None = None) -> dict[str, int]:
    """Longest consecutive run length for 0, 1, or both."""
    if not bits:
        raise ValueError("bits must be non-empty")
    if any(b not in (0, 1) for b in bits):
        raise ValueError("bits must contain only 0 and 1")

    def _longest(target: int) -> int:
        best = current = 0
        for bit in bits:
            if bit == target:
                current += 1
                best = max(best, current)
            else:
                current = 0
        return best

    if symbol is None:
        return {"longest_0": _longest(0), "longest_1": _longest(1)}
    if symbol not in (0, 1):
        raise ValueError("symbol must be 0, 1, or None")
    return {f"longest_{symbol}": _longest(symbol)}


def autocorrelation(bits: Sequence[int], max_lag: int = 20) -> dict[str, Any]:
    """Lagged autocorrelation of a binary series (Pearson on 0/1 values)."""
    if len(bits) < 2:
        raise ValueError("need at least 2 bits for autocorrelation")
    arr = np.asarray(bits, dtype=float)
    n = arr.size
    max_lag = min(max_lag, n - 1)
    mean = arr.mean()
    var = arr.var()
    lags = list(range(1, max_lag + 1))
    if var == 0:
        corrs = [float("nan")] * len(lags)
    else:
        corrs = []
        for lag in lags:
            c = np.mean((arr[: n - lag] - mean) * (arr[lag:] - mean)) / var
            corrs.append(float(c))
    return {"lags": lags, "autocorrelation": corrs, "lag1": corrs[0] if corrs else float("nan")}


def integer_histogram(integers: Sequence[int], n_bins: int) -> dict[str, Any]:
    """Histogram counts for integers expected in ``0 .. n_bins-1``."""
    if n_bins < 2:
        raise ValueError("n_bins must be >= 2")
    counts = Counter(integers)
    observed = np.array([counts.get(i, 0) for i in range(n_bins)], dtype=float)
    return {
        "bins": list(range(n_bins)),
        "observed": observed.tolist(),
        "total": int(observed.sum()),
    }


def chi_square_bit_balance(bits: Sequence[int]) -> dict[str, Any]:
    """Chi-square goodness-of-fit for fair coin bit balance."""
    freq = bit_frequency(bits)
    observed = np.array([freq["zeros"], freq["ones"]], dtype=float)
    expected = np.array([freq["n_bits"] / 2.0, freq["n_bits"] / 2.0], dtype=float)
    statistic, p_value = stats.chisquare(observed, expected)
    return {
        "test": "bit_balance_chi_square",
        "statistic": float(statistic),
        "p_value": float(p_value),
        "observed": observed.tolist(),
        "expected": expected.tolist(),
        "caveat": (
            "A non-significant p-value does not prove cryptographic security or "
            "adequate min-entropy."
        ),
    }


def chi_square_uniform_integers(
    integers: Sequence[int],
    n_bins: int,
    *,
    min_expected: float = 5.0,
) -> dict[str, Any]:
    """Chi-square uniformity test over ``0 .. n_bins-1`` with expected-count caveats."""
    hist = integer_histogram(integers, n_bins)
    observed = np.asarray(hist["observed"], dtype=float)
    total = observed.sum()
    expected = np.full(n_bins, total / n_bins, dtype=float)
    low_expected = bool(np.any(expected < min_expected))
    statistic, p_value = stats.chisquare(observed, expected)
    return {
        "test": "integer_uniformity_chi_square",
        "statistic": float(statistic),
        "p_value": float(p_value),
        "n_bins": n_bins,
        "expected_per_bin": float(expected[0]) if n_bins else 0.0,
        "low_expected_counts": low_expected,
        "caveat": (
            "Chi-square approximations degrade when expected counts are low "
            f"(threshold {min_expected}). Passing this test does not establish "
            "cryptographic security."
        ),
    }


def summarize_bit_source(name: str, bits: Sequence[int], integers: Sequence[int], n_bits: int) -> dict[str, Any]:
    """Compact comparison-row summary for one randomness source."""
    freq = bit_frequency(bits)
    runs = longest_run(bits)
    return {
        "source": name,
        "n_samples": len(integers),
        "n_bits_total": freq["n_bits"],
        "p1": freq["p1"],
        "empirical_bit_entropy": empirical_shannon_entropy(list(bits)),
        "empirical_integer_entropy": empirical_shannon_entropy(list(integers)),
        "max_integer_entropy_bits": float(n_bits),
        "longest_0": runs["longest_0"],
        "longest_1": runs["longest_1"],
        "lag1_autocorr": autocorrelation(bits, max_lag=1)["lag1"],
    }


def take(iterable: Iterable[Any], n: int) -> list[Any]:
    """Materialise the first ``n`` items (notebook convenience)."""
    return list(islice(iterable, n))


def assert_non_simulator_backend(backend: Any) -> None:
    """Fail closed if a claimed hardware backend is a simulator."""
    name = getattr(backend, "name", str(backend))
    is_sim = bool(getattr(backend, "simulator", False))
    name_l = str(name).lower()
    if is_sim or name_l.endswith("simulator") or "simulator" in name_l:
        raise RuntimeError(
            f"Refusing simulator backend in hardware mode: {name}. "
            "No silent fallback to Aer is permitted."
        )


__all__ = [
    "MAX_QUBITS",
    "MAX_SHOTS",
    "DEFAULT_QUBITS",
    "DEFAULT_SHOTS",
    "DEFAULT_SEED",
    "SIMULATOR_WARNING",
    "Provenance",
    "software_versions",
    "validate_experiment",
    "build_hadamard_qrng",
    "bitstring_to_int",
    "bits_lsb_first",
    "flatten_bits_lsb_first",
    "rejection_sample_bounded",
    "rejection_sample_many",
    "run_aer_qrng",
    "python_prng_integers",
    "python_csprng_integers",
    "integers_to_bits",
    "compare_sources",
    "bit_frequency",
    "empirical_shannon_entropy",
    "longest_run",
    "autocorrelation",
    "integer_histogram",
    "chi_square_bit_balance",
    "chi_square_uniform_integers",
    "summarize_bit_source",
    "take",
    "assert_non_simulator_backend",
]

"""Educational statistical diagnostics.

These metrics do NOT prove cryptographic security or sufficient min-entropy.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

import numpy as np
from scipy import stats


CAVEAT = (
    "Educational diagnostic only; not cryptographic certification or "
    "NIST SP 800-90B min-entropy validation."
)


def _as_bit_array(bits: list[str] | str) -> np.ndarray:
    if isinstance(bits, str):
        chars = list(bits)
    else:
        # flatten list of bitstrings or single-bit chars
        chars: list[str] = []
        for item in bits:
            chars.extend(list(item) if len(item) > 1 and set(item) <= {"0", "1"} else [item])
        chars = [c for c in chars if c in "01"]
    return np.array([1 if c == "1" else 0 for c in chars], dtype=np.int8)


def frequency_stats(bits: np.ndarray) -> dict[str, Any]:
    n = int(bits.size)
    ones = int(bits.sum())
    zeros = n - ones
    freq = ones / n if n else 0.0
    return {
        "bit_count": n,
        "zeros": zeros,
        "ones": ones,
        "frequency_ones": freq,
        "deviation_from_half": abs(freq - 0.5),
    }


def empirical_shannon_entropy(bits: np.ndarray) -> float:
    """Empirical Shannon entropy of a binary sequence (bits per symbol)."""
    n = int(bits.size)
    if n == 0:
        return 0.0
    ones = int(bits.sum())
    zeros = n - ones
    entropy = 0.0
    for count in (zeros, ones):
        if count:
            p = count / n
            entropy -= p * math.log2(p)
    return float(entropy)


def run_lengths(bits: np.ndarray) -> dict[str, Any]:
    if bits.size == 0:
        return {"longest_run": 0, "run_length_summary": {"mean": 0.0, "max": 0}, "runs": []}
    runs: list[int] = []
    current = 1
    for i in range(1, bits.size):
        if bits[i] == bits[i - 1]:
            current += 1
        else:
            runs.append(current)
            current = 1
    runs.append(current)
    return {
        "longest_run": max(runs),
        "run_length_summary": {
            "mean": float(np.mean(runs)),
            "max": int(max(runs)),
            "count": len(runs),
        },
        "runs": runs[:64],  # bounded preview
    }


def lag_autocorrelation(bits: np.ndarray, lags: list[int] | None = None) -> dict[str, float]:
    if lags is None:
        lags = [1, 2, 4, 8]
    n = int(bits.size)
    if n < 2:
        return {str(lag): 0.0 for lag in lags}
    x = bits.astype(np.float64)
    x = x - x.mean()
    var = float(np.dot(x, x))
    out: dict[str, float] = {}
    for lag in lags:
        if lag >= n or var == 0:
            out[str(lag)] = 0.0
        else:
            out[str(lag)] = float(np.dot(x[:-lag], x[lag:]) / var)
    return out


def integer_histogram(integers: list[int]) -> dict[str, int]:
    counts = Counter(integers)
    # Bound keys for JSON size
    return {str(k): int(v) for k, v in sorted(counts.items())[:512]}


def chi_square_bits(bits: np.ndarray) -> dict[str, Any]:
    """Chi-square goodness-of-fit vs fair coin — educational only."""
    n = int(bits.size)
    if n < 10:
        return {
            "stat": None,
            "p_value": None,
            "applicable": False,
            "limitation": "Sample too small for chi-square assumptions. " + CAVEAT,
        }
    ones = int(bits.sum())
    zeros = n - ones
    expected = [n / 2, n / 2]
    if min(expected) < 5:
        return {
            "stat": None,
            "p_value": None,
            "applicable": False,
            "limitation": "Expected counts < 5; chi-square not appropriate. " + CAVEAT,
        }
    stat, p = stats.chisquare([zeros, ones], f_exp=expected)
    return {
        "stat": float(stat),
        "p_value": float(p),
        "applicable": True,
        "limitation": CAVEAT,
    }


def compute_metrics(
    bit_chars: list[str] | str,
    *,
    integer_samples: list[int] | None = None,
) -> dict[str, Any]:
    bits = _as_bit_array(bit_chars)
    freq = frequency_stats(bits)
    runs = run_lengths(bits)
    ac = lag_autocorrelation(bits)
    metrics: dict[str, Any] = {
        **freq,
        "empirical_shannon_entropy_bits": empirical_shannon_entropy(bits),
        "longest_run": runs["longest_run"],
        "run_length_summary": runs["run_length_summary"],
        "lag1_autocorrelation": ac.get("1", 0.0),
        "autocorrelation": ac,
        "chi_square": chi_square_bits(bits),
        "limitation": CAVEAT,
    }
    if integer_samples is not None:
        metrics["integer_histogram"] = integer_histogram(integer_samples)
    return metrics

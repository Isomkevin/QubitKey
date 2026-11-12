"""Bitstring ordering and integer conversion helpers.

Qiskit displays measurement bitstrings with qubit 0 as the rightmost character
(little-endian). All integer conversions in QubitKey follow that convention.
"""

from __future__ import annotations

from collections import Counter


def bitstring_to_int(bitstring: str) -> int:
    """Interpret a Qiskit bitstring as an integer (qubit 0 = LSB / rightmost)."""
    cleaned = bitstring.replace(" ", "")
    if not cleaned or any(c not in "01" for c in cleaned):
        raise ValueError(f"Invalid bitstring: {bitstring!r}")
    return int(cleaned, 2)


def counts_to_samples(
    counts: dict[str, int],
    *,
    expand: bool = True,
) -> tuple[list[str], list[int]]:
    """Expand counts into sample lists (order is deterministic by sorted keys)."""
    bit_samples: list[str] = []
    integer_samples: list[int] = []
    for bitstring in sorted(counts.keys()):
        value = bitstring_to_int(bitstring)
        n = counts[bitstring]
        if expand:
            bit_samples.extend([bitstring] * n)
            integer_samples.extend([value] * n)
        else:
            bit_samples.append(bitstring)
            integer_samples.append(value)
    return bit_samples, integer_samples


def normalize_counts(counts: dict[str, int], num_qubits: int) -> dict[str, int]:
    """Zero-pad bitstrings to num_qubits and aggregate."""
    normalized: Counter[str] = Counter()
    for key, value in counts.items():
        cleaned = key.replace(" ", "")
        if len(cleaned) < num_qubits:
            cleaned = cleaned.zfill(num_qubits)
        normalized[cleaned] += int(value)
    return dict(normalized)


def rejection_sample_range(bitstrings: list[str], upper_exclusive: int) -> list[int]:
    """Map bitstrings to integers in [0, upper_exclusive) without modulo bias.

    Discards outcomes >= upper_exclusive. Requires bitstrings wide enough to
    cover the range (caller responsibility).
    """
    if upper_exclusive <= 0:
        raise ValueError("upper_exclusive must be positive")
    out: list[int] = []
    for bs in bitstrings:
        value = bitstring_to_int(bs)
        if value < upper_exclusive:
            out.append(value)
    return out

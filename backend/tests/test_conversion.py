"""Bit order and conversion tests."""

import pytest

from app.quantum.conversion import (
    bitstring_to_int,
    counts_to_samples,
    normalize_counts,
    rejection_sample_range,
)


def test_bitstring_to_int_little_endian_qubit0_rightmost():
    # Qubit 0 is rightmost: "...001" means integer 1
    assert bitstring_to_int("00000001") == 1
    assert bitstring_to_int("00000010") == 2
    assert bitstring_to_int("10110101") == 181


def test_invalid_bitstring():
    with pytest.raises(ValueError):
        bitstring_to_int("02")


def test_normalize_and_samples():
    counts = normalize_counts({"1": 2, "0": 1}, num_qubits=2)
    assert counts == {"01": 2, "00": 1}
    bits, ints = counts_to_samples(counts)
    assert len(bits) == 3
    assert set(ints) == {0, 1}


def test_rejection_sampling_no_modulo_bias():
    # 3-bit outcomes for a 6-sided die: discard 6 and 7
    samples = [format(i, "03b") for i in range(8)] * 10
    values = rejection_sample_range(samples, 6)
    assert all(0 <= v < 6 for v in values)
    assert 6 not in values and 7 not in values

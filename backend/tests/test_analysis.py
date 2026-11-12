"""Analysis metrics tests with deterministic fixtures."""

from app.analysis.metrics import compute_metrics, empirical_shannon_entropy
from app.analysis.compare import compare_sources
from app.schemas.analysis import CompareRequest
from app.schemas.common import SourceType
import numpy as np


def test_balanced_bits_entropy_near_one():
    bits = ["0", "1"] * 500
    metrics = compute_metrics(bits)
    assert metrics["bit_count"] == 1000
    assert metrics["zeros"] == 500
    assert metrics["ones"] == 500
    assert abs(metrics["empirical_shannon_entropy_bits"] - 1.0) < 1e-9
    assert metrics["chi_square"]["applicable"] is True
    assert "not cryptographic" in metrics["limitation"].lower() or "Educational" in metrics["limitation"]


def test_all_zeros_entropy_zero():
    arr = np.zeros(100, dtype=np.int8)
    assert empirical_shannon_entropy(arr) == 0.0


def test_longest_run():
    bits = list("0001111000")
    metrics = compute_metrics(bits)
    assert metrics["longest_run"] == 4


def test_compare_equal_sample_sizes():
    req = CompareRequest(
        sample_bits=256,
        qubits=4,
        sources=[SourceType.PYTHON_PRNG, SourceType.PYTHON_CSPRNG],
        seed=123,
    )
    result = compare_sources(req)
    assert result.sample_bits == 256
    assert len(result.sources) == 2
    for src in result.sources:
        assert src.metrics["bit_count"] == 256
    assert any("does not prove" in c.lower() for c in result.caveats)

"""Ensure IBM adapter never silently falls back to simulator."""

import pytest

from app.quantum.adapters.base import AdapterError
from app.quantum.adapters.ibm import IbmQpuAdapter
from app.schemas.common import SourceType


def test_ibm_unavailable_raises():
    adapter = IbmQpuAdapter()
    available, reason = adapter.is_available()
    assert available is False
    assert reason
    with pytest.raises(AdapterError) as excinfo:
        adapter.run(qubits=2, shots=8)
    assert excinfo.value.status_code == 503
    # Result must not pretend to be simulator success
    assert adapter.source_type == SourceType.IBM_QPU

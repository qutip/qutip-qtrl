import numpy as np
import pytest
import qutip

import qutip_qtrl.fidcomp as fidcomp


class _DummyDynamics:
    log_level = 30
    target = qutip.qeye(2)


@pytest.fixture
def fid_comp_unitary_su():
    fid = fidcomp.FidCompUnitary(_DummyDynamics())
    fid.phase_option = "SU"
    fid.dimensional_norm = 4.0
    return fid


def test_normalize_SU_scalar_fidelity(fid_comp_unitary_su):
    """0-d numpy scalars must not raise IndexError (see issue #40)."""
    scalar = np.array(0.75)
    result = fid_comp_unitary_su.normalize_SU(scalar)
    assert result == pytest.approx(0.75 / 4.0)


def test_normalize_SU_operator(fid_comp_unitary_su):
    """Square operators are still normalised via the trace."""
    result = fid_comp_unitary_su.normalize_SU(np.eye(2))
    assert result == pytest.approx(2.0 / 4.0)

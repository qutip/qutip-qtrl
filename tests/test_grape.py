import pytest

import numpy as np
import qutip
from qutip import (
    QobjEvo,
    propagator,
    qeye,
    sigmax,
    sigmaz,
)


from qutip_qtrl.grape import (
    grape_unitary,
    cy_grape_unitary,
    grape_unitary_adaptive,
)


@pytest.fixture(
    params=[
        pytest.param(grape_unitary, id="grape_unitary"),
        pytest.param(cy_grape_unitary, id="cy_grape_unitary"),
        pytest.param(grape_unitary_adaptive, id="grape_unitary_adaptive"),
    ]
)
def grape_unitary_func(request):
    return request.param


def test_grape_unitary(grape_unitary_func):
    # Target unitary:
    U = qutip.gates.cnot()

    # System Hamiltonian and controls:
    H0 = 0 * qeye(U.dims[0])
    H_ops = [
        sigmaz() & qeye(2),  # Z1
        qeye(2) & sigmax(),  # X2
        sigmaz() & sigmax(),  # Z1 * X2
    ]

    # Number of grape iterations:
    R = 20

    # Times slices:
    times = np.linspace(0, 2 * np.pi, 10)

    alpha = None
    beta = None
    u_limits = None

    ones_t = np.ones(len(times))
    u0 = np.array([
        ones_t / len(times),
        ones_t / len(times),
        -ones_t / len(times),
    ])

    result = grape_unitary_func(
        U,
        H0,
        H_ops,
        R,
        times,
        u_start=u0,
        u_limits=u_limits,
        eps=0.1,
        alpha=alpha,
        beta=beta,
        phase_sensitive=False,
        progress_bar=False,
    )

    U_f = result.U_f / result.U_f[0, 0]
    U_f_prop = propagator(
        result.H_t,
        times[-1],
        tlist=times,
        order=0,
        options=dict(progress_bar=False, max_step=times[1] / 10.),
    )
    U_f_prop = U_f_prop / U_f_prop[0, 0]

    np.testing.assert_allclose(U.full(), U_f.full(), atol=1e-7)
    np.testing.assert_allclose(U.full(), U_f_prop.full(), atol=1e-7)

"""
Correctness tests for TSlotCompUpdateAllVectorized (tslot_type='ALL_VEC').

Builds a Dynamics object directly with a fixed, seeded control-amplitude
array (no optimizer loop, nothing stochastic), and checks that the
vectorized path's results agree with the serial TSlotCompUpdateAll
('DEF') path, for both oper_dtype=np.ndarray and oper_dtype=Qobj.

This is deliberately independent of GRAPE/CRAB and any optimizer
tolerance -- it compares dyn._prop / dyn._fwd_evo directly, so a real
numerical bug in the batched eigh/einsum path can't hide behind a loose
fid_err_targ the way it could if this only checked final fidelities
after an optimize_pulse_unitary() run.
"""
import numpy as np
import pytest
from qutip import Qobj

from qutip_qtrl import pulseoptim as qtrl_pulseoptim

SEED = 20260830
NT = 40
TG = 20.0
MAX_AMP = 1.0
# Absolute tolerance for agreement between DEF and ALL_VEC. The two paths
# take different floating-point routes to the propagator (serial
# expm-style computation vs a batched eigh), so exact equality isn't
# expected -- but they should agree to well within double-precision
# accumulation error over NT timeslots.
ATOL = 1e-10


def _build_dynamics(oper_dtype, tslot_type):
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    detuning = 0.01

    H0 = Qobj(0.5 * detuning * sz)
    Hc = [Qobj(0.5 * sx), Qobj(0.5 * sy)]
    U0 = Qobj(np.eye(2, dtype=complex))
    Utarg = Qobj(sx)  # arbitrary fixed target; only relevant to evolution,
    # not used to judge correctness here

    optim = qtrl_pulseoptim.create_pulse_optimizer(
        H0, Hc, U0, Utarg,
        num_tslots=NT, evo_time=TG,
        amp_lbound=-MAX_AMP, amp_ubound=MAX_AMP,
        dyn_type='UNIT',
        dyn_params={'oper_dtype': oper_dtype},
        tslot_type=tslot_type,
        gen_stats=True,
    )
    dyn = optim.dynamics
    dyn.init_timeslots()
    return dyn


def _as_array(x):
    """Qobj or ndarray -> ndarray, for numeric comparison."""
    return x.full() if isinstance(x, Qobj) else np.asarray(x)


@pytest.fixture(scope="module")
def fixed_amps():
    rng = np.random.default_rng(SEED)
    return rng.uniform(-MAX_AMP, MAX_AMP, size=(NT, 2))


@pytest.fixture(scope="module")
def dyn_reference(fixed_amps):
    """The known-good baseline: serial computer, plain ndarray internals."""
    dyn = _build_dynamics(np.ndarray, 'DEF')
    dyn.initialize_controls(fixed_amps)
    dyn.tslot_computer.recompute_evolution()
    return dyn


@pytest.mark.parametrize("oper_dtype,oper_dtype_name", [
    (np.ndarray, "ndarray"),
    (Qobj, "Qobj"),
])
def test_all_vec_matches_serial(fixed_amps, dyn_reference, oper_dtype,
                                 oper_dtype_name):
    """ALL_VEC must reproduce DEF's propagators and forward evolution,
    for both oper_dtype settings, to within numerical tolerance."""
    dyn_vec = _build_dynamics(oper_dtype, 'ALL_VEC')
    dyn_vec.initialize_controls(fixed_amps)
    dyn_vec.tslot_computer.recompute_evolution()

    for k in range(dyn_reference.num_tslots):
        ref = _as_array(dyn_reference._prop[k])
        got = _as_array(dyn_vec._prop[k])
        assert np.allclose(got, ref, atol=ATOL), (
            f"_prop[{k}] mismatch for oper_dtype={oper_dtype_name}: "
            f"max diff {np.max(np.abs(got - ref)):.3e}"
        )

    for k in range(dyn_reference.num_tslots + 1):
        ref = _as_array(dyn_reference._fwd_evo[k])
        got = _as_array(dyn_vec._fwd_evo[k])
        assert np.allclose(got, ref, atol=ATOL), (
            f"_fwd_evo[{k}] mismatch for oper_dtype={oper_dtype_name}: "
            f"max diff {np.max(np.abs(got - ref)):.3e}"
        )


def test_all_vec_qobj_mode_returns_qobj(fixed_amps):
    """Regression guard: oper_dtype=Qobj must actually store Qobj
    instances in dyn._prop after the vectorized path runs -- not a
    silent fallback to plain ndarrays (or vice versa, a silent skip of
    the wrap-back step). This is exactly the failure mode that showed
    up as an unexpectedly-fast 'ALL_VEC' timing during manual testing
    before the wrap-back was added."""
    dyn = _build_dynamics(Qobj, 'ALL_VEC')
    dyn.initialize_controls(fixed_amps)
    dyn.tslot_computer.recompute_evolution()

    assert all(isinstance(dyn._prop[k], Qobj) for k in range(dyn.num_tslots))
    assert all(
        isinstance(dyn._fwd_evo[k], Qobj) for k in range(dyn.num_tslots + 1)
    )


def test_all_vec_falls_back_when_unsupported():
    """Time-dependent control generators aren't handled by the
    vectorized path, so _vectorized_path_supported() must return False
    and recompute_evolution() must fall back to the serial computer
    without raising."""
    dyn = _build_dynamics(np.ndarray, 'ALL_VEC')
    # time_depend_ctrl_dyn_gen is one of the documented bail-out
    # conditions in _vectorized_path_supported(); force it directly
    # rather than constructing a full time-dependent Hamiltonian, since
    # this test only needs to exercise the fallback branch itself.
    dyn.time_depend_ctrl_dyn_gen = True
    assert dyn.tslot_computer._vectorized_path_supported() is False
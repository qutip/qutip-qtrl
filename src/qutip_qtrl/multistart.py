# @author: Sashreek Satapathy
# @email1: sashreeksatapathydpsnt15@gmail.com
# @email2: sashreeksatapathy@gmail.com
# @organization: Delhi Public School Vadodara, India
# @supervisor: Veronika Kurth, RIKEN and Dr. Boxi Li, RIKEN
"""

qutip_qtrl.multistart
======================

Multi-core parallel multi-start optimization for qutip_qtrl's pulse
optimizers.

optimize_pulse_unitary() is commonly called repeatedly with different random
initial pulses ("multi-start"), since both GRAPE (a local optimizer,
sensitive to its starting point) and especially CRAB (a randomized
direct-search method, where restart diversity matters even more) can land
on different local optima from run to run. Today that has to be done with a
plain Python loop, one restart after another.

This module runs the restarts concurrently across a process pool instead.
Each restart is a fully independent optimize_pulse_unitary() call: no shared
state and no communication between restarts, so this parallelizes for free
on any multi-core machine. The benefit is largest for algorithms or
configurations that vectorization/JIT-style optimizations cannot reach --
CRAB in particular, since it is gradient-free and therefore never engages
the exact-propagator-gradient-dependent optimizations (e.g.
tslotcomp.TSlotCompUpdateAllVectorized, if present in this build) that speed
up GRAPE. Restart-level parallelism helps CRAB regardless.

Caller responsibility (standard for any multiprocessing use on macOS/
Windows, not specific to this module): code that calls
optimize_pulse_unitary_multistart() from a script must guard the call with

    if __name__ == "__main__":
        ...

since these platforms use the 'spawn' start method, which re-imports the
calling script in every worker process.
"""

import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, Sequence, List, Tuple, Any

import numpy as np

from qutip_qtrl import pulseoptim as _pulseoptim

__all__ = ["optimize_pulse_unitary_multistart", "MultistartResult"]


class MultistartResult:
    """Aggregated result of a multi-start optimization run.

    Attributes
    ----------
    best : Result
        The qutip_qtrl Result object with the lowest fid_err across all
        restarts.
    all_results : list of (restart_index, seed, Result)
        Every restart's outcome, in restart-index order regardless of the
        order in which restarts actually completed.
    wall_time : float
        Total wall-clock time for the whole multistart call (the elapsed
        time you'd actually observe, not the sum of each restart's own
        wall_time -- that sum is available via
        sum(r.wall_time for _, _, r in all_results) if wanted for
        comparison against a serial run).
    """

    def __init__(
        self,
        best: Any,
        all_results: List[Tuple[int, int, Any]],
        wall_time: float,
    ):
        self.best = best
        self.all_results = all_results
        self.wall_time = wall_time

    @property
    def fid_err(self) -> float:
        return self.best.fid_err

    @property
    def final_amps(self) -> np.ndarray:
        return self.best.final_amps


def _multistart_worker(args):
    (
        H_d,
        H_c,
        U_0,
        U_targ,
        restart_idx,
        seed,
        init_pulse_type,
        tslot_type,
        kwargs,
    ) = args

    np.random.seed(seed)

    # --- tslot_type workaround -------------------------------------------
    # At least as of the qutip_qtrl release this was written against,
    # optimize_pulse_unitary() accepts a tslot_type= argument and forwards
    # it through create_pulse_optimizer(), but nothing in that call chain
    # ever applies it to the internal OptimConfig object -- OptimConfig
    # .__init__ hardcodes tslot_type = "DEF" and nothing downstream
    # overrides it (confirmed by direct inspection of optimconfig.py /
    # pulseoptim.py; see the accompanying patch to pulseoptim.py that fixes
    # this properly at the source). Patched narrowly here, inside the
    # worker process only, so this module works correctly even before that
    # fix lands. Safe to delete this block once the real fix is applied.
    if tslot_type is not None:
        import qutip_qtrl.optimconfig as _optimconfig

        if not getattr(
            _optimconfig.OptimConfig, "_multistart_tslot_patched", False
        ):
            _orig_init = _optimconfig.OptimConfig.__init__

            def _patched_init(self, *a, **kw):
                _orig_init(self, *a, **kw)
                self.tslot_type = tslot_type

            _optimconfig.OptimConfig.__init__ = _patched_init
            _optimconfig.OptimConfig._multistart_tslot_patched = True
    # -----------------------------------------------------------------------

    res = _pulseoptim.optimize_pulse_unitary(
        H_d,
        H_c,
        U_0,
        U_targ,
        init_pulse_type=init_pulse_type,
        **kwargs,
    )
    return restart_idx, seed, res


def optimize_pulse_unitary_multistart(
    H_d,
    H_c,
    U_0,
    U_targ,
    n_restarts: int = 4,
    n_workers: Optional[int] = None,
    init_pulse_types: Optional[Sequence[str]] = None,
    seed_base: Optional[int] = None,
    tslot_type: Optional[str] = None,
    pool: Optional[ProcessPoolExecutor] = None,
    **kwargs,
) -> MultistartResult:
    """Run n_restarts independent optimize_pulse_unitary() calls concurrently
    across a process pool and return the best one.

    Parameters
    ----------
    H_d, H_c, U_0, U_targ :
        Same meaning as in optimize_pulse_unitary.
    n_restarts : int
        Number of independent restarts. Each gets its own random initial
        pulse (unless init_pulse_types is given explicitly) and its own RNG
        seed, so restarts explore genuinely different starting points
        rather than repeating the same optimization n_restarts times.
    n_workers : int, optional
        Process pool size. Defaults to min(n_restarts, os.cpu_count()).
    init_pulse_types : sequence of str, optional
        Per-restart init_pulse_type values (the same strings
        optimize_pulse_unitary accepts, e.g. 'DEF', 'RNDFOURIER'). If
        omitted, restart 0 uses 'DEF' and the rest use 'RNDFOURIER' --
        one "sensible default" start plus diverse random starts, a common
        multi-start convention.
    seed_base : int, optional
        Restart r is seeded with seed_base + r. Defaults to a
        time-derived value if omitted -- pass an explicit value for
        reproducible runs, e.g. when comparing against a serial multi-start
        loop and expecting the same winning restart.
    tslot_type : str, optional
        Forwarded to every restart. See the workaround note in
        _multistart_worker if the installed qutip_qtrl doesn't apply this
        argument correctly on its own.
    pool : ProcessPoolExecutor, optional
        Reuse an existing pool instead of creating and tearing down a new
        one for this call -- useful when this function is called repeatedly,
        e.g. inside a sweep over gate times.
    **kwargs :
        Forwarded to every optimize_pulse_unitary() call: num_tslots,
        evo_time, amp_lbound, amp_ubound, fid_err_targ, max_iter, alg,
        alg_params, gen_stats, etc.

    Returns
    -------
    MultistartResult
        .best is the Result with the lowest fid_err across all restarts.
        .all_results holds every restart's (index, seed, Result).

    Notes
    -----
    This parallelizes ACROSS restarts (each fully independent), not WITHIN
    a single restart's internal per-timeslot loop -- that is a separate,
    unrelated optimization (see tslotcomp.TSlotCompUpdateAllVectorized, if
    present in this build). The two compose: passing tslot_type='ALL_VEC'
    here gets both a faster per-restart evaluation for gradient-based
    algorithms AND concurrent restarts, but the restart-level speedup this
    function provides is what actually benefits gradient-free algorithms
    like CRAB, which cannot use the vectorized path at all (CRAB does not
    compute or cache the exact propagator gradients that path requires).
    """
    t0 = time.time()

    if init_pulse_types is None:
        init_pulse_types = [
            "DEF" if r == 0 else "RNDFOURIER" for r in range(n_restarts)
        ]
    if len(init_pulse_types) != n_restarts:
        raise ValueError(
            f"init_pulse_types has {len(init_pulse_types)} entries but "
            f"n_restarts={n_restarts}"
        )
    if seed_base is None:
        seed_base = int(time.time() * 1000) % (2**31)
    if n_workers is None:
        n_workers = min(n_restarts, os.cpu_count() or 1)

    owns_pool = pool is None
    if owns_pool:
        pool = ProcessPoolExecutor(max_workers=n_workers)

    try:
        args_list = [
            (
                H_d,
                H_c,
                U_0,
                U_targ,
                r,
                seed_base + r,
                init_pulse_types[r],
                tslot_type,
                kwargs,
            )
            for r in range(n_restarts)
        ]
        futures = {pool.submit(_multistart_worker, a): a[4] for a in args_list}
        all_results: List[Optional[Tuple[int, int, Any]]] = [None] * n_restarts
        for fut in as_completed(futures):
            restart_idx, seed, res = fut.result()
            all_results[restart_idx] = (restart_idx, seed, res)
    finally:
        if owns_pool:
            pool.shutdown(wait=True)

    best = min((r for _, _, r in all_results), key=lambda r: r.fid_err)
    return MultistartResult(best, all_results, time.time() - t0)

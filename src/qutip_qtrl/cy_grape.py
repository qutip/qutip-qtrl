""" Fast routines for grape implemented on top of the data layer. """

import qutip.core.data as _data


def cy_overlap(op1, op2):
    """
    Return the overlap of op1 and op2.

    Parameters
    ----------
    op1 : :class:`qutip.data.Data`
        Data layer representation of first operator.
    op2 : :class:`qutip.data.Data`
        Data layer representation of second operator.

    Result
    ------
    overlap : float
        The value of the overlap.
    """
    return _data.trace(_data.adjoint(op1) @ op2) / op1.shape[0]


def cy_grape_inner(
    U,
    u,
    r,
    J,
    M,
    U_b_list,
    U_f_list,
    H_ops,
    dt,
    eps,
    alpha,
    beta,
    phase_sensitive,
    use_u_limits,
    u_min,
    u_max,
):
    """
    Perform one iteration of GRAPE control pulse
    updates.

    Parameters
    ----------
    U : :class:`qutip.data.Data`
        The target unitary.

    u : np.ndarray
        The generated control pulses. It's shape
        is (iterations, controls, times), i.e.
        (R, J, M). The result of this iteration
        is stored in u[r, :, :].

    r : int
        The number of this GRAPE iteration.

    J : int
        The number of controls in the Hamiltonian.

    M : int
        The number of times.

    U_b_list : list of :class:`qutip.data.Data`
        The backward propagators for each time.
        The list has length M.

    U_f_list : list of :class:`qutip.data.Data`
        The forward propagators for each time.
        The list has length M.

    H_ops : list of :class:`qutip.data.Data`
        The control operators from the Hamiltonian.
        The list has length J.

    dt : float
        The time step.

    eps : float
        The distance to move along the gradient when updating
        the controls.

    alpha : float
        The penalty to apply to higher power control signals.

    beta : float
        The penalty to apply to later control signals.

    phase_sensitive : bool
        Whether the overlap is phase sensitive.

    use_u_limits : bool
        Whether to apply limits to the control amplitudes.

    u_min : float
        Minimum control amplitude.

    u_max : float
        Maximum control amplitude.

    Result
    ------
    The results are stored in u[r + 1, : , :].
    """
    for m in range(M - 1):
        P = U_b_list[m] @ U
        for j in range(J):
            Q = 1j * dt * H_ops[j] @ U_f_list[m]

            if phase_sensitive:
                du = -cy_overlap(P, Q)
            else:
                du = -2 * cy_overlap(P, Q) * cy_overlap(U_f_list[m], P)

            if alpha > 0.0:
                # penalty term for high power control signals u
                du += -2 * alpha * u[r, j, m] * dt

            if beta:
                # penalty term for late control signals u
                du += -2 * beta * m**2 * u[r, j, m] * dt

            u[r + 1, j, m] = u[r, j, m] + eps * du.real

            if use_u_limits:
                if u[r + 1, j, m] < u_min:
                    u[r + 1, j, m] = u_min
                elif u[r + 1, j, m] > u_max:
                    u[r + 1, j, m] = u_max

    for j in range(J):
        u[r + 1, j, M - 1] = u[r + 1, j, M - 2]

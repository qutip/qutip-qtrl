*********
Changelog
*********


Version 0.1.0 (March 12, 2023)
++++++++++++++++++++++++++++++

This is the first release of qutip-qtrl, the quantum control package in QuTiP.

The qutip-qtrl package used to be a module ``qutip.control`` under `QuTiP (Quantum Toolbox in Python) <http://qutip.org/index.html>`_. From QuTiP 5.0, the community has decided to decrease the size of the core QuTiP package by reducing the external dependencies, in order to simplify maintenance. Hence a few modules are separated from the core QuTiP and will become QuTiP family packages. They are still maintained by the QuTiP team but hosted under different repositories in the `QuTiP organization <https://github.com/qutip>`_.

The qutip-qtrl package, QuTiP quantum optimal control, aims at providing advanced tools for the optimal control of quantum devices.

Features
--------

- The `cy_grape_unitary` optimizer now uses the QuTiP 5 data layer directly and no longer requires Cython. The `cy_grape` module remains available for compatibility, but also no longer uses Cython.

Bug Fixes
---------

- The `grape_unitary_adaptive` optimizer previously overwrote the target unitary with the identity. It no longer does this.

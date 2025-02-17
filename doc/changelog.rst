*********
Changelog
*********

Version 0.1.4 (February 10, 2025)
+++++++++++++++++++++++++++++

This patch implements changes necessary to support numpy v2.

Miscellaneous
-------------

- Increase the sampling points in tests for pulse optimization (#27, Boxi Li).


Version 0.1.3 (June 24, 2024)
+++++++++++++++++++++++++++++

This patch fixes some conflicts due to changes in QuTiP v5.
No Python 3.8 support any more.

Miscellaneous
-------------

- Integrate qutip v5 changes (#23, Patrick Hopf).


Version 0.1.2 (June 11, 2024)
+++++++++++++++++++++++++++++

This is a patch release of qutip-qtrl that provides updates to support the QuTiP-QOC 0.1.0.b0 release.

Miscellaneous
-------------

- Fix a typo in PulseGenTriangle.gen_pulse docs (#17, Huai-Ming Yu).


Features
--------

- Add frequencies as optional CRAB parameter (#18 Patrick Hopf).


Bug Fixes
---------

- Bugfix for method_params (#19, Patrick Hopf).


Version 0.1.1 (February 12, 2024)
+++++++++++++++++++++++++++++++++

This is a patch release of qutip-qtrl that provides updates to support the QuTiP 5.0.0a2 release.

Bug Fixes
---------

- Fixed progress bar initialization and usage (#13, #15, Patrick Hopf).
- Replaced the logging utilities that were removed from QuTiP v5 with a vendored copy in this package (#9, #10, Èric Giguere, Boxi Li).
- Applied black to setup.py and doc/conf.py scripts (#8, Simon Cross).


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

# qutip-qtrl

[![build](https://github.com/qutip/qutip-qtrl/workflows/Tests/badge.svg)](https://github.com/qutip/qutip-qtrl/actions)
[![Documentation Status](https://readthedocs.org/projects/qutip-qtrl/badge/?version=stable)](https://qutip-qtrl.readthedocs.io/en/stable/)
[![PyPI version](https://badge.fury.io/py/qutip-qtrl.svg)](https://badge.fury.io/py/qutip-qtrl)
[![Maintainability](https://api.codeclimate.com/v1/badges/30293d7b8eb249f8d679/maintainability)](https://codeclimate.com/github/qutip/qutip-qtrl/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/qutip/qutip-qtrl/badge.svg)](https://coveralls.io/github/qutip/qutip-qtrl)

The qutip-qtrl package used to be a module ``qutip.control`` under [QuTiP (Quantum Toolbox in Python)](http://qutip.org/index.html).
From QuTiP 5.0, the community has decided to decrease the size of the core QuTiP package by reducing the external dependencies, in order to simplify maintenance.
Hence a few modules are separated from the core QuTiP and will become QuTiP family packages.
They are still maintained by the QuTiP team but hosted under different repositories in the [QuTiP organization](https://github.com/qutip).

The qutip-qtrl package, QuTiP quantum optimal control, aims at providing advanced tools for the optimal control of quantum devices.
Compared to other libraries for quantum optimal control, qutip-qtrl puts additional emphasis on the physics layer and the interaction with the QuTiP package.
The package offers support for both the CRAB and GRAPE methods.

If you would like to know the future development plan and ideas, have a look at the [qutip documentation for ideas](https://qutip.org/docs/latest/development/ideas.html).

Quick start
-----------
To install the package, use
```
pip install qutip-qtrl
```

Migrating from ``qutip.control``
--------------------------------
As the introduction suggested, this package is based on a module in the [QuTiP](http://qutip.org/docs/latest/) package `qutip.control`.
If you were using the `qutip` package and now want to try out the new features included in this package, you can simply install this package and replace all the `qutip.control` in your import statement with `qutip_qtrl`. Everything should work smoothly as usual.

Documentation and tutorials
---------------------------
The documentation of `qutip-qtrl` updated to the latest development version is hosted at [qutip-qtrl.readthedocs.io/](https://qutip-qtrl.readthedocs.io/en/stable/).
Tutorials related to using quantum optimal control in `qutip-qtrl` can be found [*here*](https://qutip.org/qutip-tutorials/#optimal-control).

Installation from source
------------------------
If you want to edit the source code, please download the source code and run the following command under the root `qutip-qtrl` folder,
```
pip install --upgrade pip
pip install -e .
```
which makes sure that you are up to date with the latest `pip` version. Contribution guidelines are available [*here*](https://qutip-qtrl.readthedocs.io/en/latest/contribution-code.html).

To build and test the documentation, additional packages need to be installed:

```
pip install pytest matplotlib sphinx numpydoc sphinx_rtd_theme
```

Under the `doc` directory, use
```
make html
```
to build the documentation, or
```
make doctest
```
to test the code in the documentation.

Testing
-------
To test the installation, choose the correct branch that matches with the version, e.g., `qutip-qtrl-0.2.X` for version 0.2. Then download the source code and run from the `qutip-qtrl` directory.
```
pytest tests
```

Citing `qutip-qtrl`
-------------------
If you use `qutip-qtrl` in your research, please cite the original QuTiP papers that are available [here](https://dml.riken.jp/?s=QuTiP).

Support
-------
This package is supported and maintained by the same developers group as QuTiP.

[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.org)
[![Unitary Fund](https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=flat)](https://unitary.fund)

QuTiP development is supported by [Nori's lab](http://dml.riken.jp/)
at RIKEN, by the University of Sherbrooke, by Chalmers University of Technology, by Macquarie University and by Aberystwyth University,
[among other supporting organizations](http://qutip.org/#supporting-organizations).

License
-------
[![license](https://img.shields.io/badge/license-New%20BSD-blue.svg)](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29)

You are free to use this software, with or without modification, provided that the conditions listed in the LICENSE.txt file are satisfied.

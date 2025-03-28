"""Tests for qutip_qtrl.family."""

import re

from qutip_qtrl import family


class TestVersion:
    def test_version(self):
        pkg, version = family.version()
        assert pkg == "qutip-qtrl"
        assert re.match(r"\d+\.\d+\.\d+.*", version)

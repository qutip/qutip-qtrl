from configparser import ConfigParser

import numpy as np
import pytest
from qutip import Qobj

import qutip_qtrl.loadparams as loadparams


class _Holder:
    def __init__(self):
        self.q = Qobj(np.eye(2))
        self.arr = np.zeros(2)
        self.lst = [1.0]
        self.flt = 1.0
        self.cpx = 1j
        self.i = 1
        self.b = True


def _parser(attr, value):
    parser = ConfigParser()
    parser.read_string("[s]\n{} = {}\n".format(attr, value))
    return parser


@pytest.mark.parametrize(
    "attr, bad_value, message",
    [
        ("q", "[[1,0],[0]]", "generate a Qobj"),
        ("q", "foo", "generate a Qobj"),
        ("arr", "[1,'a']", "generate an ndarray"),
        ("lst", "5", "generate a list"),
        ("flt", "1/0", "cast or evaluated as a float"),
        ("cpx", "abc", "cast as complex"),
        ("i", "2.5", "cast as an int"),
        ("b", "maybe", "cast as a bool"),
    ],
)
def test_bad_value_raises_value_error(attr, bad_value, message):
    parser = _parser(attr, bad_value)
    with pytest.raises(ValueError, match=message):
        loadparams.set_param(parser, "s", attr, _Holder(), attr)


@pytest.mark.parametrize(
    "attr, value, expected",
    [
        ("flt", "2*3", 6.0),
        ("i", "3", 3),
        ("b", "false", False),
        ("cpx", "1+2j", 1 + 2j),
    ],
)
def test_valid_values_are_set(attr, value, expected):
    obj = _Holder()
    loadparams.set_param(_parser(attr, value), "s", attr, obj, attr)
    assert getattr(obj, attr) == expected


def test_untyped_attribute_falls_back_to_string():
    obj = _Holder()
    obj.other = None
    loadparams.set_param(_parser("other", "hello"), "s", "other", obj, "other")
    assert obj.other == "hello"


@pytest.mark.parametrize(
    "attr, method",
    [("i", "getint"), ("b", "getboolean"), ("flt", "getfloat")],
)
def test_keyboard_interrupt_is_not_swallowed(attr, method, monkeypatch):
    parser = _parser(attr, "1")

    def interrupted(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(parser, method, interrupted)
    with pytest.raises(KeyboardInterrupt):
        loadparams.set_param(parser, "s", attr, _Holder(), attr)

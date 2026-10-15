import inspect

from qutip_qtrl import logging_utils


def test_get_logger_uses_caller_module_name_without_stack(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("get_logger() must not build the full stack")

    monkeypatch.setattr(inspect, "stack", fail)
    assert logging_utils.get_logger().name == __name__

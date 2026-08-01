import pytest

from exceptions import KillSwitchActiveError


def test_exception_is_tos_exception():
    assert issubclass(
        KillSwitchActiveError,
        Exception,
    )


def test_exception_message():
    error = KillSwitchActiveError("Trading stopped")

    assert str(error) == "Trading stopped"


def test_exception_can_be_raised():
    with pytest.raises(KillSwitchActiveError):
        raise KillSwitchActiveError("Stop")


def test_exception_can_be_caught():
    try:
        raise KillSwitchActiveError("Stop")
    except KillSwitchActiveError:
        assert True


def test_exception_is_instance():
    error = KillSwitchActiveError("Stop")

    assert isinstance(error, KillSwitchActiveError)


def test_exception_repr():
    error = KillSwitchActiveError("Stop")

    assert "Stop" in repr(error)


def test_empty_message():
    error = KillSwitchActiveError("")

    assert str(error) == ""


def test_long_message():
    message = "Trading halted due to emergency."

    error = KillSwitchActiveError(message)

    assert str(error) == message


def test_multiple_instances():
    first = KillSwitchActiveError("A")
    second = KillSwitchActiveError("B")

    assert first != second


def test_exception_args():
    error = KillSwitchActiveError("Stop")

    assert error.args == ("Stop",)

import pytest

from operations.startup.validator import StartupValidator


class PassingValidator:
    def validate(self):
        return True


class FailingValidator:
    def validate(self):
        raise ValueError("Validation failed")


def test_register_validator():
    startup = StartupValidator()

    startup.register(PassingValidator())

    assert len(startup._checks) == 1


def test_multiple_validators():
    startup = StartupValidator()

    startup.register(PassingValidator())
    startup.register(PassingValidator())
    startup.register(PassingValidator())

    assert len(startup._checks) == 3


def test_all_validators_pass():
    startup = StartupValidator()

    startup.register(PassingValidator())
    startup.register(PassingValidator())

    result = startup.run()

    assert result.success is True


def test_first_failure_stops():
    startup = StartupValidator()

    startup.register(PassingValidator())
    startup.register(FailingValidator())
    startup.register(PassingValidator())

    result = startup.run()

    assert result.success is False


def test_no_validators():
    startup = StartupValidator()

    result = startup.run()

    assert result.success is True


def test_register_returns_none():
    startup = StartupValidator()

    returned = startup.register(PassingValidator())

    assert returned is None


def test_run_multiple_times():
    startup = StartupValidator()

    startup.register(PassingValidator())

    assert startup.run().success
    assert startup.run().success


def test_failure_message():
    startup = StartupValidator()

    startup.register(FailingValidator())

    result = startup.run()

    assert "Validation failed" in result.message


def test_validator_order():
    order = []

    class A:
        def validate(self):
            order.append("A")
            return True

    class B:
        def validate(self):
            order.append("B")
            return True

    startup = StartupValidator()

    startup.register(A())
    startup.register(B())

    startup.run()

    assert order == ["A", "B"]


def test_empty_validator():
    startup = StartupValidator()

    class Empty:
        def validate(self):
            pass

    startup.register(Empty())

    result = startup.run()

    assert result.success is True
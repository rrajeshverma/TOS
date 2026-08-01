from runtime.safety_factory import SafetyFactory
from safety.composite_execution_guard import (
    CompositeExecutionGuard,
)


def test_factory_returns_composite_guard():
    assert isinstance(
        SafetyFactory.create(),
        CompositeExecutionGuard,
    )


def test_factory_guard_can_execute():
    assert SafetyFactory.create().can_execute()


def test_factory_returns_new_instance():
    first = SafetyFactory.create()
    second = SafetyFactory.create()

    assert first is not second


def test_factory_returns_boolean():
    assert isinstance(
        SafetyFactory.create().can_execute(),
        bool,
    )


def test_multiple_factory_calls():
    for _ in range(5):
        assert SafetyFactory.create().can_execute()


def test_factory_is_repeatable():
    first = SafetyFactory.create().can_execute()
    second = SafetyFactory.create().can_execute()

    assert first == second


def test_factory_creates_valid_guard():
    guard = SafetyFactory.create()

    assert guard.can_execute() is True


def test_factory_guard_type():
    assert type(SafetyFactory.create()) is CompositeExecutionGuard


def test_factory_never_returns_none():
    assert SafetyFactory.create() is not None


def test_factory_can_build_many():
    guards = [SafetyFactory.create() for _ in range(10)]

    assert len(guards) == 10

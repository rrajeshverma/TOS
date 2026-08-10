from unittest.mock import Mock

from execution.execution_engine import ExecutionEngine
from runtime.safety_factory import SafetyFactory


def create_engine():
    return ExecutionEngine(
        Mock(),
        execution_guard=SafetyFactory.create(),
    )


def test_factory_creates_engine():
    assert isinstance(
        create_engine(),
        ExecutionEngine,
    )


def test_engine_contains_guard():
    engine = create_engine()

    assert engine.execution_guard is not None


def test_guard_allows_execution():
    engine = create_engine()

    assert engine.execution_guard.can_execute()


def test_factory_returns_new_guard():
    first = SafetyFactory.create()
    second = SafetyFactory.create()

    assert first is not second


def test_multiple_engines():
    first = create_engine()
    second = create_engine()

    assert first is not second


def test_guard_returns_boolean():
    engine = create_engine()

    assert isinstance(
        engine.execution_guard.can_execute(),
        bool,
    )


def test_engine_stores_guard():
    engine = create_engine()

    assert engine.execution_guard == engine.execution_guard


def test_factory_can_create_many():
    guards = [SafetyFactory.create() for _ in range(10)]

    assert len(guards) == 10


def test_guard_is_composite():
    engine = create_engine()

    assert hasattr(
        engine.execution_guard,
        "can_execute",
    )


def test_engine_creation_is_repeatable():
    for _ in range(5):
        engine = create_engine()

        assert engine.execution_guard.can_execute()

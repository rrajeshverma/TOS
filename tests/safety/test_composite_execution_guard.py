from unittest.mock import Mock

from safety.composite_execution_guard import (
    CompositeExecutionGuard,
)


def guard(result: bool):
    g = Mock()
    g.can_execute.return_value = result
    return g


def test_empty_guard_list_allows_execution():
    assert CompositeExecutionGuard([]).can_execute()


def test_single_true_guard():
    assert CompositeExecutionGuard([guard(True)]).can_execute()


def test_single_false_guard():
    assert CompositeExecutionGuard([guard(False)]).can_execute() is False


def test_two_true_guards():
    assert CompositeExecutionGuard([guard(True), guard(True)]).can_execute()


def test_first_false_guard():
    assert CompositeExecutionGuard([guard(False), guard(True)]).can_execute() is False


def test_second_false_guard():
    assert CompositeExecutionGuard([guard(True), guard(False)]).can_execute() is False


def test_three_true_guards():
    assert CompositeExecutionGuard(
        [
            guard(True),
            guard(True),
            guard(True),
        ]
    ).can_execute()


def test_multiple_false_guards():
    assert (
        CompositeExecutionGuard(
            [
                guard(False),
                guard(False),
            ]
        ).can_execute()
        is False
    )


def test_every_guard_called():
    first = guard(True)
    second = guard(True)

    CompositeExecutionGuard([first, second]).can_execute()

    first.can_execute.assert_called_once()
    second.can_execute.assert_called_once()


def test_result_is_boolean():
    assert isinstance(
        CompositeExecutionGuard([]).can_execute(),
        bool,
    )

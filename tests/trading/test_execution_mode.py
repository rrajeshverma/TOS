from trading.execution_mode import (
    ExecutionMode,
    ExecutionModeGuard,
)


def test_default_mode_is_paper():

    guard = ExecutionModeGuard()

    assert (
        guard.mode
        == ExecutionMode.PAPER
    )


def test_paper_mode_allows_execution():

    guard = ExecutionModeGuard(
        ExecutionMode.PAPER
    )

    assert (
        guard.can_execute()
        is True
    )


def test_live_mode_requires_enable():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    assert (
        guard.can_execute()
        is False
    )


def test_live_mode_after_enable():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    guard.enable_live_trading()

    assert (
        guard.can_execute()
        is True
    )


def test_emergency_disable_blocks_live():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    guard.enable_live_trading()

    guard.disable_live_trading()

    assert (
        guard.can_execute()
        is False
    )

from safety.trade_limit_guard import TradeLimitGuard


def test_allows_trades_until_limit():
    guard = TradeLimitGuard(max_trades=4)

    assert guard.can_execute()
    guard.record_execution()

    assert guard.can_execute()
    guard.record_execution()

    assert guard.can_execute()
    guard.record_execution()

    assert guard.can_execute()
    guard.record_execution()

    assert not guard.can_execute()


def test_failed_execution_does_not_consume_slot():
    guard = TradeLimitGuard(max_trades=2)

    assert guard.can_execute()
    assert guard.submitted == 0

    guard.record_execution()

    assert guard.submitted == 1
    assert guard.can_execute()


def test_starts_empty():
    guard = TradeLimitGuard(max_trades=4)

    assert guard.submitted == 0
    assert guard.can_execute()

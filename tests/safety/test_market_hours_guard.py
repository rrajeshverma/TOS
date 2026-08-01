from safety.market_hours_guard import MarketHoursGuard


def test_guard_starts_open():
    assert MarketHoursGuard().can_execute()


def test_guard_can_start_closed():
    assert (
        MarketHoursGuard(
            market_open=False,
        ).can_execute()
        is False
    )


def test_close_market_blocks_execution():
    guard = MarketHoursGuard()

    guard.close_market()

    assert guard.can_execute() is False


def test_open_market_allows_execution():
    guard = MarketHoursGuard(
        market_open=False,
    )

    guard.open_market()

    assert guard.can_execute()


def test_close_then_open():
    guard = MarketHoursGuard()

    guard.close_market()
    guard.open_market()

    assert guard.can_execute()


def test_multiple_close_calls():
    guard = MarketHoursGuard()

    guard.close_market()
    guard.close_market()

    assert guard.can_execute() is False


def test_multiple_open_calls():
    guard = MarketHoursGuard(
        market_open=False,
    )

    guard.open_market()
    guard.open_market()

    assert guard.can_execute()


def test_instances_are_independent():
    first = MarketHoursGuard()
    second = MarketHoursGuard()

    first.close_market()

    assert first.can_execute() is False
    assert second.can_execute()


def test_can_execute_returns_bool():
    assert isinstance(
        MarketHoursGuard().can_execute(),
        bool,
    )


def test_guard_is_reusable():
    guard = MarketHoursGuard()

    for _ in range(5):
        guard.close_market()
        guard.open_market()

    assert guard.can_execute()

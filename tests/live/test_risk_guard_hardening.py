from live.risk_guard import RiskGuard


def test_default_allows_trade():

    guard = RiskGuard()

    assert guard.can_trade()


def test_daily_loss_block():

    guard = RiskGuard(
        daily_loss_limit=1000
    )

    guard.record_loss(1500)

    assert not guard.can_trade()


def test_position_limit():

    guard = RiskGuard(
        max_positions=2
    )

    guard.add_position()
    guard.add_position()

    assert not guard.can_open_position()


def test_trade_block():

    guard = RiskGuard()

    guard.block()

    assert not guard.can_trade()


def test_trade_allow():

    guard = RiskGuard()

    guard.allow()

    assert guard.can_trade()
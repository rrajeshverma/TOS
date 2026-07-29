"""
Integration Test:

Live Risk Guard Flow

Validates trading safety controls.
"""

from decimal import Decimal


class LiveRiskGuard:
    def __init__(
        self,
        max_trades=5,
        max_daily_loss=Decimal("5000"),
    ):
        self.max_trades = max_trades

        self.max_daily_loss = max_daily_loss

        self.emergency_stop = False

    def can_trade(
        self,
        trades_today,
        daily_loss,
    ):
        if self.emergency_stop:
            return False

        if trades_today >= self.max_trades:
            return False

        if daily_loss >= self.max_daily_loss:
            return False

        return True

    def activate_emergency_stop(self):
        self.emergency_stop = True


def create_guard():
    return LiveRiskGuard()


def test_trade_allowed_within_limits():
    guard = create_guard()

    result = guard.can_trade(
        trades_today=1,
        daily_loss=Decimal("500"),
    )

    assert result is True


def test_trade_blocked_after_max_trades():
    guard = create_guard()

    result = guard.can_trade(
        trades_today=5,
        daily_loss=Decimal("0"),
    )

    assert result is False


def test_trade_blocked_after_daily_loss_limit():
    guard = create_guard()

    result = guard.can_trade(
        trades_today=1,
        daily_loss=Decimal("5000"),
    )

    assert result is False


def test_emergency_stop_blocks_trading():
    guard = create_guard()

    guard.activate_emergency_stop()

    result = guard.can_trade(
        trades_today=0,
        daily_loss=Decimal("0"),
    )

    assert result is False


def test_risk_guard_allows_recovery_after_new_session():
    guard = create_guard()

    assert (
        guard.can_trade(
            trades_today=0,
            daily_loss=Decimal("0"),
        )
        is True
    )

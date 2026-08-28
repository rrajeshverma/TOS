from datetime import datetime
from decimal import Decimal

from backtesting.backtest_context import BacktestContext
from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.position_size import PositionSize
from domain.risk import Risk
from domain.trade_plan import TradePlan
from shared.enums import DecisionStatus, Signal


def create_risk(signal=Signal.BUY_CE):
    market = Market(
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="30m",
        timestamp=datetime(2026, 1, 1, 0, 0),
        open=100,
        high=105,
        low=95,
        close=100,
        volume=1000,
    )

    decision = Decision(
        decision_id="D1",
        timestamp=market.timestamp,
        market=market,
        indicator_set=IndicatorSet(
            ema_high=101,
            ema_low=99,
            vwap=100,
            rsi=60,
        ),
        signal=signal,
        status=DecisionStatus.VALID,
        reasons=(),
    )

    return Risk(
        decision=decision,
        approved=True,
        reasons=(),
    )


def create_market(
    timestamp,
    close,
):
    return Market(
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="30m",
        timestamp=timestamp,
        open=close,
        high=close,
        low=close,
        close=close,
        volume=1000,
    )


def test_on_risk_opens_trade_with_trade_parameters():
    context = BacktestContext()

    risk = create_risk()

    trade_plan = TradePlan(
        decision=risk.decision,
        position_size=PositionSize(
            quantity=65,
            lots=1,
            risk_amount=Decimal("650"),
        ),
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target_price=Decimal("120"),
    )

    context.on_risk(
        risk=risk,
        market=create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
        trade_plan=trade_plan,
    )

    trade = context.trade_executor.current_trade

    assert trade is not None
    assert trade.entry_price == Decimal("100")
    assert trade.quantity == 65


def test_on_risk_signal_reversal_uses_new_trade_plan():
    context = BacktestContext()

    buy_risk = create_risk(Signal.BUY_CE)

    buy_plan = TradePlan(
        decision=buy_risk.decision,
        position_size=PositionSize(
            quantity=65,
            lots=1,
            risk_amount=Decimal("650"),
        ),
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target_price=Decimal("120"),
    )

    context.on_risk(
        risk=buy_risk,
        market=create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
        trade_plan=buy_plan,
    )

    sell_risk = create_risk(Signal.BUY_PE)

    sell_plan = TradePlan(
        decision=sell_risk.decision,
        position_size=PositionSize(
            quantity=130,
            lots=2,
            risk_amount=Decimal("1300"),
        ),
        entry_price=Decimal("110"),
        stop_loss=Decimal("120"),
        target_price=Decimal("90"),
    )

    context.on_risk(
        risk=sell_risk,
        market=create_market(
            datetime(2026, 1, 1, 0, 30),
            110,
        ),
        trade_plan=sell_plan,
    )

    trade = context.trade_executor.current_trade

    assert trade is not None
    assert trade.entry_price == Decimal("110")
    assert trade.quantity == 130
    assert trade.stop_loss == Decimal("120")
    assert trade.target == Decimal("90")


def test_on_risk_signal_reversal_records_closed_trade_once():
    context = BacktestContext()

    buy_risk = create_risk(Signal.BUY_CE)

    buy_plan = TradePlan(
        decision=buy_risk.decision,
        position_size=PositionSize(
            quantity=65,
            lots=1,
            risk_amount=Decimal("650"),
        ),
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target_price=Decimal("120"),
    )

    context.on_risk(
        risk=buy_risk,
        market=create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
        trade_plan=buy_plan,
    )

    sell_risk = create_risk(Signal.BUY_PE)

    sell_plan = TradePlan(
        decision=sell_risk.decision,
        position_size=PositionSize(
            quantity=130,
            lots=2,
            risk_amount=Decimal("1300"),
        ),
        entry_price=Decimal("110"),
        stop_loss=Decimal("120"),
        target_price=Decimal("90"),
    )

    context.on_risk(
        risk=sell_risk,
        market=create_market(
            datetime(2026, 1, 1, 0, 30),
            110,
        ),
        trade_plan=sell_plan,
    )

    assert context.trade_ledger.total_trades == 1
    assert context.trade_ledger.trades[0].status.value == "CLOSED"


def test_finalize_does_not_duplicate_closed_trade():
    context = BacktestContext()

    risk = create_risk()

    trade_plan = TradePlan(
        decision=risk.decision,
        position_size=PositionSize(
            quantity=65,
            lots=1,
            risk_amount=Decimal("650"),
        ),
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target_price=Decimal("120"),
    )

    market = create_market(
        datetime(2026, 1, 1, 0, 0),
        100,
    )

    context.on_risk(
        risk=risk,
        market=market,
        trade_plan=trade_plan,
    )

    context.finalize(market)
    context.finalize(market)

    assert context.trade_ledger.total_trades == 1
    assert context.trade_ledger.trades[0].exit_reason.value == "END_OF_DATA"

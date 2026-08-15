from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

from backtesting.historical_data_feed import HistoricalDataFeed
from backtesting.replay_runner import ReplayRunner
from domain.market import Market
from domain.position_size import PositionSize
from domain.trade_plan import TradePlan
from shared.enums import Signal


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


def create_trade_plan():
    position_size = PositionSize(
        quantity=65,
        lots=1,
        risk_amount=Decimal("650"),
    )

    return TradePlan(
        decision=MagicMock(),
        position_size=position_size,
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        target_price=Decimal("120"),
    )


def test_replay_runner_feeds_runtime():
    runtime = MagicMock()
    runtime.on_market_tick.return_value = None

    markets = [
        create_market(
            datetime(2026, 1, 1, 0, 0),
            104,
        ),
        create_market(
            datetime(2026, 1, 1, 0, 30),
            105,
        ),
    ]

    feed = HistoricalDataFeed(markets)

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
    )

    runner.run()

    assert runtime.on_market_tick.call_count == 2


def test_replay_runner_passes_trade_plan_to_context():
    runtime = MagicMock()
    runtime.on_market_tick.return_value = MagicMock()

    trade_plan = create_trade_plan()
    runtime.last_trade_plan = trade_plan

    context = MagicMock()

    markets = [
        create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
    ]

    feed = HistoricalDataFeed(markets)

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
        context=context,
    )

    runner.run()

    context.on_risk.assert_called_once_with(
        risk=runtime.on_market_tick.return_value,
        market=markets[0],
        trade_plan=trade_plan,
    )


def test_replay_runner_closes_trade_on_target():
    runtime = MagicMock()

    risk = MagicMock()
    risk.is_approved = True
    risk.decision.signal = Signal.BUY_CE

    runtime.on_market_tick.return_value = risk

    trade_plan = create_trade_plan()
    runtime.last_trade_plan = trade_plan

    context = MagicMock()

    markets = [
        create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
        Market(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
            timestamp=datetime(2026, 1, 1, 0, 30),
            open=100,
            high=121,
            low=100,
            close=110,
            volume=1000,
        ),
    ]

    feed = HistoricalDataFeed(markets)

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
        context=context,
    )

    runner.run()

    assert context.on_market.call_count == 2
    assert context.on_risk.call_count == 2


def test_replay_runner_real_context_closes_trade_on_target():
    runtime = MagicMock()

    risk = MagicMock()
    risk.is_approved = True
    risk.decision.signal = MagicMock()

    runtime.on_market_tick.return_value = risk
    runtime.last_trade_plan = create_trade_plan()

    markets = [
        create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
        Market(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
            timestamp=datetime(2026, 1, 1, 0, 30),
            open=100,
            high=121,
            low=100,
            close=110,
            volume=1000,
        ),
    ]

    feed = HistoricalDataFeed(markets)

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
    )

    processed = runner.run()

    assert processed == 2
    assert runner.context.trade_ledger.total_trades == 1

    trade = runner.context.trade_ledger.trades[0]

    assert trade.status.value == "CLOSED"
    assert trade.entry_price == Decimal("100")
    assert trade.exit_price == Decimal("120")
    assert trade.target == Decimal("120")


def test_replay_runner_keeps_trade_open_when_no_exit():
    runtime = MagicMock()

    risk = MagicMock()
    risk.is_approved = True
    risk.decision.signal = Signal.BUY_CE

    runtime.on_market_tick.return_value = risk
    runtime.last_trade_plan = create_trade_plan()

    markets = [
        create_market(
            datetime(2026, 1, 1, 0, 0),
            100,
        ),
        Market(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
            timestamp=datetime(2026, 1, 1, 0, 30),
            open=100,
            high=105,
            low=98,
            close=103,
            volume=1000,
        ),
        Market(
            symbol="BTCUSDT",
            exchange="BINANCE",
            timeframe="30m",
            timestamp=datetime(2026, 1, 1, 1, 0),
            open=103,
            high=108,
            low=101,
            close=106,
            volume=1000,
        ),
    ]

    feed = HistoricalDataFeed(markets)

    runner = ReplayRunner(
        runtime=runtime,
        feed=feed,
    )

    processed = runner.run()

    assert processed == 3
    assert runner.context.trade_ledger.total_trades == 1

    trade = runner.context.trade_ledger.trades[0]

    assert trade.status.value == "CLOSED"
    assert trade.entry_price == Decimal("100")
    assert trade.exit_reason.value == "END_OF_DATA"

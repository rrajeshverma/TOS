from datetime import datetime
from decimal import Decimal

from domain.market import Market
from domain.indicator_set import IndicatorSet

from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory

from services.paper_trading_service import PaperTradingService

from shared.enums import TradeStatus


def create_trade():

    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24990,
        high=25010,
        low=24980,
        close=25000,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )

    return TradeFactory().create(
        risk=risk,
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24950"),
    )


def test_execute_trade():

    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    assert position.quantity == 65
    assert position.average_price == Decimal("25000")
    assert position.last_traded_price == Decimal("25000")
    assert position.status == TradeStatus.OPEN


def test_update_price():

    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    updated = service.update_price(
        position,
        Decimal("25025"),
    )

    assert updated.last_traded_price == Decimal("25025")


def test_close_position():

    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    closed = service.close(
        position,
        Decimal("25100"),
    )

    assert closed.status == TradeStatus.CLOSED
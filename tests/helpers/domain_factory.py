from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.portfolio import Portfolio
from domain.position_size import PositionSize
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory
from engines.trade_quality_engine import TradeQualityEngine


def make_market(
    *,
    close=Decimal(25000),
    open=Decimal(24990),
    high=Decimal(25010),
    low=Decimal(24980),
    volume=100000,
    symbol="NIFTY",
    exchange="NSE",
    timeframe="5m",
    timestamp=None,
):
    return Market(
        symbol=symbol,
        exchange=exchange,
        timeframe=timeframe,
        timestamp=timestamp or datetime(2026, 8, 18, 11, 0),
        open=open,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def make_indicator_set(
    *,
    ema_high=24950,
    ema_low=24850,
    vwap=24900,
    rsi=60,
    volume_average=100000,
):
    return IndicatorSet(
        ema_high=ema_high,
        ema_low=ema_low,
        vwap=vwap,
        rsi=rsi,
        volume_average=volume_average,
    )


def make_decision():
    """
    Create a valid strategy decision.
    """

    market = make_market()

    indicators = make_indicator_set()

    return DecisionEngine().evaluate(
        market,
        indicators,
    )


def make_trade():
    market = make_market()

    indicators = make_indicator_set()

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
        entry_price=Decimal(25000),
        stop_loss=Decimal(24950),
    )


def make_portfolio():
    return Portfolio(
        account_id="ACC001",
        cash=100000.0,
        available_margin=90000.0,
        used_margin=10000.0,
        equity=100000.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0,
        positions=0,
        holdings=0,
    )


def make_trade_quality():
    """
    Create a valid TradeQuality object.
    """

    decision = make_decision()

    return TradeQualityEngine().evaluate(
        decision=decision,
        trades_today=0,
    )


def make_risk():
    """
    Create a valid Risk object.
    """

    decision = make_decision()

    return RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )


def make_position_size():
    """
    Create a valid PositionSize object.
    """

    return PositionSize(
        lots=2,
        quantity=130,
        risk_amount=Decimal(1300),
    )

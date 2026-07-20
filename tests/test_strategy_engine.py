from datetime import datetime, timedelta

from engines.strategy_engine import StrategyEngine
from shared.enums import Signal


def create_raw_market(price: float):
    return {
        "symbol": "NIFTY",
        "exchange": "NSE",
        "timeframe": "5m",
        "timestamp": datetime.now(),
        "open": price - 5,
        "high": price + 10,
        "low": price - 10,
        "close": price,
        "volume": 100000,
    }


from domain.market import Market


def create_history():
    history = []

    start = datetime(2026, 1, 1, 9, 15)

    for i in range(40):

        history.append(
            Market(
                symbol="NIFTY",
                exchange="NSE",
                timeframe="5m",
                timestamp=start + timedelta(minutes=i * 5),
                open=24000 + i,
                high=24002 + i,
                low=23998 + i,
                close=24001 + i,
                volume=100000 + i * 100,
            )
        )

    return history


def test_strategy_engine_pipeline():

    engine = StrategyEngine()

    raw_market = create_raw_market(24050)

    history = create_history()

    decision = engine.evaluate(
        raw_market,
        history,
    )

    assert decision.signal in (
        Signal.NONE,
        Signal.BUY_CE,
        Signal.BUY_PE,
    )

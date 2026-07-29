from decimal import Decimal
from unittest.mock import Mock

from brokers.dhan.models import BrokerTick
from services.market_data_service import MarketDataService

from domain.market_tick import MarketTick

from datetime import datetime

def test_market_tick():
    tick = MarketTick(
        symbol="NIFTY",
        ltp=Decimal("25123.45"),
        volume=100,
        timestamp="2026-07-29T09:15:00",
    )

    assert tick.symbol == "NIFTY"
    assert tick.ltp == Decimal("25123.45")
    assert tick.volume == 100
    assert tick.timestamp == "2026-07-29T09:15:00"

def test_to_market_tick():
    websocket = Mock()

    service = MarketDataService(websocket)

    broker_tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000.0,
        volume=10,
        timestamp=datetime(2026, 7, 29, 9, 15),
    )

    tick = service.to_market_tick(broker_tick)

    assert tick.symbol == "NIFTY"
    assert tick.ltp == Decimal("25000")
    assert tick.volume == 10

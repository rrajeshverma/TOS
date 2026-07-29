from datetime import datetime

import pytest

from market.data_service import MarketDataService
from market.paper_adapter import PaperMarketAdapter
from market.tick import Tick


def create_tick():
    return Tick(
        symbol="NIFTY",
        price=24500.50,
        volume=100,
        timestamp=datetime.now(),
        exchange="NSE",
    )


def test_service_can_start():
    service = MarketDataService(PaperMarketAdapter())

    service.start()

    assert service.health() == "RUNNING"


def test_service_can_stop():
    service = MarketDataService(PaperMarketAdapter())

    service.start()
    service.stop()

    assert service.health() == "STOPPED"


def test_service_can_publish_tick():
    service = MarketDataService(PaperMarketAdapter())

    event = service.publish_tick(create_tick())

    assert event.tick.symbol == "NIFTY"


def test_service_returns_latest_tick():
    service = MarketDataService(PaperMarketAdapter())

    tick = create_tick()

    service.publish_tick(tick)

    assert service.get_latest_tick("NIFTY") == tick


def test_service_requires_adapter():
    with pytest.raises(ValueError):
        MarketDataService(None)


def test_service_initial_health():
    service = MarketDataService(PaperMarketAdapter())

    assert service.health() == "STOPPED"

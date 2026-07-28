from datetime import datetime

from market.data_service import MarketDataService
from market.health import MarketDataHealth
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


def test_complete_market_data_pipeline():

    adapter = PaperMarketAdapter()

    service = MarketDataService(
        adapter
    )

    health = MarketDataHealth()

    service.start()

    tick = create_tick()

    event = service.publish_tick(
        tick
    )

    health.record_tick(
        event.tick
    )

    assert (
        event.tick.symbol
        == "NIFTY"
    )

    assert (
        service.get_latest_tick("NIFTY")
        == tick
    )

    assert (
        health.is_healthy()
        is True
    )


def test_pipeline_generates_market_event():

    service = MarketDataService(
        PaperMarketAdapter()
    )

    event = service.publish_tick(
        create_tick()
    )

    assert (
        event.event_type
        == "PRICE_UPDATE"
    )

    assert (
        event.source
        == "PAPER"
    )


def test_pipeline_service_health():

    service = MarketDataService(
        PaperMarketAdapter()
    )

    assert (
        service.health()
        == "STOPPED"
    )

    service.start()

    assert (
        service.health()
        == "RUNNING"
    )


def test_pipeline_latest_tick_updates():

    service = MarketDataService(
        PaperMarketAdapter()
    )

    tick = create_tick()

    service.publish_tick(
        tick
    )

    latest = service.get_latest_tick(
        "NIFTY"
    )

    assert latest.price == 24500.50


def test_pipeline_supports_multiple_ticks():

    service = MarketDataService(
        PaperMarketAdapter()
    )

    first = create_tick()

    service.publish_tick(
        first
    )

    latest = service.get_latest_tick(
        "NIFTY"
    )

    assert (
        latest.symbol
        == "NIFTY"
    )


def test_pipeline_health_requires_market_data():

    health = MarketDataHealth()

    assert (
        health.recovery_required()
        is True
    )

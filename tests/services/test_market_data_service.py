from datetime import datetime
from decimal import Decimal

from brokers.dhan.models import BrokerTick
from domain.market_tick import MarketTick

from unittest.mock import Mock

from services.market_data_service import MarketDataService


def test_connect():
    websocket = Mock()

    service = MarketDataService(websocket)

    service.connect()

    websocket.connect.assert_called_once()


def test_disconnect():
    websocket = Mock()

    service = MarketDataService(websocket)

    service.disconnect()

    websocket.disconnect.assert_called_once()


def test_subscribe():
    websocket = Mock()

    service = MarketDataService(websocket)

    service.subscribe("NIFTY")

    websocket.subscribe.assert_called_once_with("NIFTY")


def test_unsubscribe():
    websocket = Mock()

    service = MarketDataService(websocket)

    service.unsubscribe("NIFTY")

    websocket.unsubscribe.assert_called_once_with("NIFTY")


def test_clear_subscriptions():
    websocket = Mock()

    service = MarketDataService(websocket)

    service.clear_subscriptions()

    websocket.clear_subscriptions.assert_called_once()


def test_register_tick_callback():
    websocket = Mock()

    service = MarketDataService(websocket)

    handler = Mock()

    service.register_tick_callback(handler)

    websocket.register_tick_callback.assert_called_once_with(handler)


def test_is_connected():
    websocket = Mock()
    websocket.is_connected = True

    service = MarketDataService(websocket)

    assert service.is_connected is True


def test_subscriptions():
    websocket = Mock()
    websocket.subscriptions = {"NIFTY", "BANKNIFTY"}

    service = MarketDataService(websocket)

    assert service.subscriptions == {
        "NIFTY",
        "BANKNIFTY",
    }

def test_to_market_tick():
    websocket = Mock()
    service = MarketDataService(websocket)

    broker_tick = BrokerTick(
        symbol="NIFTY",
        ltp=25001.25,
        volume=123,
        timestamp=datetime.now(),
    )

    tick = service.to_market_tick(broker_tick)

    assert isinstance(tick, MarketTick)
    assert tick.symbol == "NIFTY"
    assert tick.ltp == Decimal("25001.25")
    assert tick.volume == 123
    assert tick.timestamp == broker_tick.timestamp

def test_emit_market_tick():
    websocket = Mock()

    callback = Mock()
    websocket.tick_callback = callback

    service = MarketDataService(websocket)

    broker_tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000,
        volume=5,
        timestamp=datetime.now(),
    )

    service.emit_market_tick(broker_tick)

    callback.assert_called_once()

    market_tick = callback.call_args.args[0]

    assert market_tick.symbol == "NIFTY"
    assert market_tick.ltp == Decimal("25000")
    assert market_tick.volume == 5

def test_emit_market_tick_without_callback():
    websocket = Mock()
    websocket.tick_callback = None

    service = MarketDataService(websocket)

    broker_tick = BrokerTick(
        symbol="NIFTY",
        ltp=25000,
        volume=5,
        timestamp=datetime.now(),
    )

    service.emit_market_tick(broker_tick)
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


def test_register_tick_handler():
    websocket = Mock()

    service = MarketDataService(websocket)

    handler = Mock()

    service.register_tick_handler(handler)

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

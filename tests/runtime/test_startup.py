from unittest.mock import Mock, patch

import pytest

from config.runtime_config import RuntimeConfig
from exceptions import InvalidConfigurationError
from runtime.startup import Startup


def test_startup_loads_broker():
    startup = Startup(RuntimeConfig())
    startup.load_broker("paper")
    assert startup.config.broker == "paper"


def test_startup_loads_portfolio():
    startup = Startup(RuntimeConfig())
    startup.load_portfolio("default")
    assert startup.config.portfolio == "default"


def test_startup_initializes_services():
    startup = Startup(RuntimeConfig())
    startup.initialize_services()
    assert startup.services_initialized is True


def test_initialize_services_creates_market_data_service():
    startup = Startup(RuntimeConfig())
    startup.initialize_services()
    assert "market_data_service" in startup.services


def test_startup_rejects_invalid_runtime_config():
    startup = Startup(RuntimeConfig(broker="invalid"))

    with pytest.raises(InvalidConfigurationError):
        startup.initialize_services()


def test_shutdown_stops_runtime():
    startup = Startup(RuntimeConfig())

    runtime = Mock()
    broker = Mock()

    startup.services = {
        "trading_runtime": runtime,
        "broker": broker,
    }

    startup.services_initialized = True

    startup.shutdown()

    runtime.stop.assert_called_once()


def test_shutdown_disconnects_broker():
    startup = Startup(RuntimeConfig())

    runtime = Mock()
    broker = Mock()

    startup.services = {
        "trading_runtime": runtime,
        "broker": broker,
    }

    startup.shutdown()

    broker.disconnect.assert_called_once()


def test_initialize_uses_paper_broker():
    startup = Startup(
        RuntimeConfig(broker="paper"),
    )

    startup.initialize_services()

    broker = startup.services["broker"]

    assert broker.__class__.__name__ == "PaperBroker"


@patch("runtime.startup.DhanBroker")
@patch("runtime.startup.DhanClient")
def test_initialize_registers_dhan_client(
    mock_client,
    mock_broker,
):
    startup = Startup(
        RuntimeConfig(broker="dhan"),
    )

    startup.initialize_services()

    assert "dhan_client" in startup.services


@patch("runtime.startup.WebSocketClient")
@patch("runtime.startup.LiveMarketFeed")
@patch("runtime.startup.DhanInstrumentProvider")
def test_initialize_uses_dhan_market_data_with_paper_broker(
    mock_provider,
    mock_live_feed,
    mock_websocket,
):
    mock_provider.return_value.load.return_value = []

    startup = Startup(
        RuntimeConfig(
            broker="paper",
            market_data="dhan",
            mode="PAPER",
        ),
    )

    startup.initialize_services()

    mock_live_feed.assert_called_once()
    mock_websocket.assert_called_once()

    market_data_service = startup.services["market_data_service"]

    assert market_data_service.websocket is mock_websocket.return_value


def test_startup_initial_state():
    startup = Startup()

    assert startup.services == {}
    assert startup.services_initialized is False


def test_shutdown_marks_services_uninitialized():
    startup = Startup()

    startup.services = {
        "trading_runtime": Mock(),
        "broker": Mock(),
    }

    startup.services_initialized = True

    startup.shutdown()

    assert startup.services_initialized is False


@patch("runtime.startup.LOGGER")
def test_log_banner(mock_logger):
    startup = Startup()

    startup.log_banner()

    assert mock_logger.info.called


@patch("runtime.startup.LOGGER")
def test_log_health(mock_logger):
    startup = Startup()

    broker = Mock()
    broker.is_connected.return_value = True

    runtime = Mock()
    runtime.state = "RUNNING"

    startup.services = {
        "broker": broker,
        "trading_runtime": runtime,
    }

    startup.log_health()

    assert mock_logger.info.called

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

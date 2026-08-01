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

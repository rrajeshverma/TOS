from runtime.startup import Startup


def test_startup_loads_broker():
    startup = Startup()
    startup.load_broker("paper")
    assert startup.broker == "paper"


def test_startup_loads_portfolio():
    startup = Startup()
    startup.load_portfolio("default")
    assert startup.portfolio == "default"


def test_startup_initializes_services():
    startup = Startup()
    startup.initialize_services()
    assert startup.services_initialized is True

def test_initialize_services_creates_market_data_service():
    startup = Startup()

    startup.initialize_services()

    assert "market_data_service" in startup.services
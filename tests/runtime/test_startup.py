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

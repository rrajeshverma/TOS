"""
Integration Test:

TOS Production Startup Flow

Validates:

START
 |
 +-- Configuration
 |
 +-- Authentication
 |
 +-- Market Feed
 |
 +-- Runtime
 |
STOP
"""


class ProductionRuntime:

    def __init__(self):

        self.config_loaded = False
        self.authenticated = False
        self.market_connected = False
        self.running = False


    def load_config(self):

        self.config_loaded = True


    def authenticate(self):

        if not self.config_loaded:
            raise RuntimeError(
                "Configuration required"
            )

        self.authenticated = True


    def connect_market(self):

        if not self.authenticated:
            raise RuntimeError(
                "Authentication required"
            )

        self.market_connected = True


    def start(self):

        if not self.market_connected:
            raise RuntimeError(
                "Market connection required"
            )

        self.running = True


    def stop(self):

        self.running = False

        self.market_connected = False


def create_runtime():

    return ProductionRuntime()


def start_production_runtime():

    runtime = create_runtime()

    runtime.load_config()

    runtime.authenticate()

    runtime.connect_market()

    runtime.start()

    return runtime


def test_configuration_loads_before_start():

    runtime = create_runtime()

    runtime.load_config()

    assert (
        runtime.config_loaded
        is True
    )


def test_authentication_requires_configuration():

    runtime = create_runtime()

    try:

        runtime.authenticate()

    except RuntimeError:

        assert True

    else:

        assert False


def test_market_requires_authentication():

    runtime = create_runtime()

    runtime.load_config()

    try:

        runtime.connect_market()

    except RuntimeError:

        assert True

    else:

        assert False


def test_production_runtime_starts():

    runtime = start_production_runtime()

    assert (
        runtime.running
        is True
    )

    assert (
        runtime.market_connected
        is True
    )


def test_production_runtime_shutdown():

    runtime = start_production_runtime()

    runtime.stop()

    assert (
        runtime.running
        is False
    )

    assert (
        runtime.market_connected
        is False
    )

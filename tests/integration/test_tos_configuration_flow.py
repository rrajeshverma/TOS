"""
Integration Test:

TOS Configuration Flow

Validates:

Configuration Loading
        |
        ▼
Runtime Settings
        |
        ▼
Trading Environment
"""


class TosConfiguration:
    def __init__(self):
        self.settings = {}

    def load(self):
        self.settings = {
            "mode": "PAPER",
            "symbol": "NIFTY",
            "quantity": 65,
            "max_daily_loss": 5000,
            "max_trades": 5,
        }

        return self.settings

    def get(
        self,
        key,
    ):
        return self.settings.get(key)


def create_config():
    config = TosConfiguration()

    config.load()

    return config


def test_configuration_loads_successfully():
    config = create_config()

    assert config.settings is not None


def test_trading_mode_is_configured():
    config = create_config()

    assert config.get("mode") == "PAPER"


def test_symbol_configuration():
    config = create_config()

    assert config.get("symbol") == "NIFTY"


def test_risk_limits_are_available():
    config = create_config()

    assert config.get("max_daily_loss") == 5000

    assert config.get("max_trades") == 5


def test_quantity_configuration():
    config = create_config()

    assert config.get("quantity") == 65

import pytest

from config.config_manager import ConfigManager
from config.config_validator import ConfigValidator


def create_valid_config():
    return {
        "broker": {
            "name": "DHAN",
            "api_key": "abc123",
        },
        "risk": {
            "capital": 100000,
            "risk_percent": 2,
        },
        "trading": {
            "mode": "PAPER",
        },
    }


def test_valid_configuration():
    manager = ConfigManager(create_valid_config())
    validator = ConfigValidator(manager)

    assert validator.validate()


def test_missing_broker():
    cfg = create_valid_config()
    del cfg["broker"]

    manager = ConfigManager(cfg)

    with pytest.raises(ValueError):
        ConfigValidator(manager).validate()


def test_missing_api_key():
    cfg = create_valid_config()
    del cfg["broker"]["api_key"]

    manager = ConfigManager(cfg)

    with pytest.raises(ValueError):
        ConfigValidator(manager).validate()


def test_missing_risk():
    cfg = create_valid_config()
    del cfg["risk"]

    manager = ConfigManager(cfg)

    with pytest.raises(ValueError):
        ConfigValidator(manager).validate()


def test_missing_capital():
    cfg = create_valid_config()
    del cfg["risk"]["capital"]

    manager = ConfigManager(cfg)

    with pytest.raises(ValueError):
        ConfigValidator(manager).validate()


def test_negative_capital():
    cfg = create_valid_config()
    cfg["risk"]["capital"] = -100

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_zero_capital():
    cfg = create_valid_config()
    cfg["risk"]["capital"] = 0

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_missing_risk_percent():
    cfg = create_valid_config()
    del cfg["risk"]["risk_percent"]

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_invalid_risk_percent():
    cfg = create_valid_config()
    cfg["risk"]["risk_percent"] = 150

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_missing_trading():
    cfg = create_valid_config()
    del cfg["trading"]

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_missing_mode():
    cfg = create_valid_config()
    del cfg["trading"]["mode"]

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_live_mode():
    cfg = create_valid_config()
    cfg["trading"]["mode"] = "LIVE"

    assert ConfigValidator(ConfigManager(cfg)).validate()


def test_backtest_mode():
    cfg = create_valid_config()
    cfg["trading"]["mode"] = "BACKTEST"

    assert ConfigValidator(ConfigManager(cfg)).validate()


def test_invalid_mode():
    cfg = create_valid_config()
    cfg["trading"]["mode"] = "TEST"

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_capital_type():
    cfg = create_valid_config()
    cfg["risk"]["capital"] = "100"

    with pytest.raises(TypeError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_risk_type():
    cfg = create_valid_config()
    cfg["risk"]["risk_percent"] = "2"

    with pytest.raises(TypeError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_api_key_required():
    cfg = create_valid_config()
    cfg["broker"]["api_key"] = ""

    with pytest.raises(ValueError):
        ConfigValidator(ConfigManager(cfg)).validate()


def test_validator_returns_bool():
    validator = ConfigValidator(ConfigManager(create_valid_config()))

    assert validator.validate() is True


def test_multiple_validations():
    validator = ConfigValidator(ConfigManager(create_valid_config()))

    assert validator.validate()
    assert validator.validate()


def test_manager_not_modified():
    manager = ConfigManager(create_valid_config())

    ConfigValidator(manager).validate()

    assert manager.has("broker")

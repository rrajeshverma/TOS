import pytest

from config.config_manager import ConfigManager
from brokers.risk_validator import RiskValidator


def create_valid_config():
    return {
        "risk": {
            "capital": 100000,
            "risk_percent": 2,
            "daily_loss_limit": 5000,
            "max_trades": 5,
            "max_open_positions": 2,
            "risk_reward_ratio": 2,
        }
    }


def test_valid_configuration():
    validator = RiskValidator(ConfigManager(create_valid_config()))
    assert validator.validate()


def test_missing_risk():
    with pytest.raises(ValueError):
        RiskValidator(ConfigManager({})).validate()


def test_missing_capital():
    cfg = create_valid_config()
    del cfg["risk"]["capital"]

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_missing_risk_percent():
    cfg = create_valid_config()
    del cfg["risk"]["risk_percent"]

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_missing_daily_loss_limit():
    cfg = create_valid_config()
    del cfg["risk"]["daily_loss_limit"]

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_missing_max_trades():
    cfg = create_valid_config()
    del cfg["risk"]["max_trades"]

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_missing_max_open_positions():
    cfg = create_valid_config()
    del cfg["risk"]["max_open_positions"]

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_missing_rr():
    cfg = create_valid_config()
    del cfg["risk"]["risk_reward_ratio"]

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


@pytest.mark.parametrize(
    "field",
    [
        "capital",
        "daily_loss_limit",
        "max_trades",
        "max_open_positions",
        "risk_reward_ratio",
    ],
)
def test_negative_values(field):
    cfg = create_valid_config()
    cfg["risk"][field] = -1

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_invalid_risk_percent():
    cfg = create_valid_config()
    cfg["risk"]["risk_percent"] = 150

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_zero_capital():
    cfg = create_valid_config()
    cfg["risk"]["capital"] = 0

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_zero_daily_loss():
    cfg = create_valid_config()
    cfg["risk"]["daily_loss_limit"] = 0

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_zero_max_trades():
    cfg = create_valid_config()
    cfg["risk"]["max_trades"] = 0

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_zero_positions():
    cfg = create_valid_config()
    cfg["risk"]["max_open_positions"] = 0

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_zero_rr():
    cfg = create_valid_config()
    cfg["risk"]["risk_reward_ratio"] = 0

    with pytest.raises(ValueError):
        RiskValidator(ConfigManager(cfg)).validate()


def test_returns_true():
    validator = RiskValidator(ConfigManager(create_valid_config()))
    assert validator.validate() is True


def test_multiple_runs():
    validator = RiskValidator(ConfigManager(create_valid_config()))

    assert validator.validate()
    assert validator.validate()


def test_manager_not_modified():
    manager = ConfigManager(create_valid_config())

    RiskValidator(manager).validate()

    assert manager.has("risk")
import pytest

from config.config_manager import ConfigManager
from strategies.strategy_validator import StrategyValidator


def create_valid_config():
    return {
        "strategy": {
            "name": "ORB",
            "enabled": True,
            "timeframe": "5m",
            "entry_rules": ["VWAP", "EMA33"],
            "exit_rules": ["SL", "TP"],
            "indicators": ["VWAP", "EMA33", "RSI"],
            "position_sizing": "fixed",
        }
    }


def test_valid_strategy():
    validator = StrategyValidator(ConfigManager(create_valid_config()))
    assert validator.validate()


def test_missing_strategy():
    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager({})).validate()


def test_missing_name():
    cfg = create_valid_config()
    del cfg["strategy"]["name"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_missing_enabled():
    cfg = create_valid_config()
    del cfg["strategy"]["enabled"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_missing_timeframe():
    cfg = create_valid_config()
    del cfg["strategy"]["timeframe"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_missing_entry_rules():
    cfg = create_valid_config()
    del cfg["strategy"]["entry_rules"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_missing_exit_rules():
    cfg = create_valid_config()
    del cfg["strategy"]["exit_rules"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_missing_indicators():
    cfg = create_valid_config()
    del cfg["strategy"]["indicators"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_missing_position_sizing():
    cfg = create_valid_config()
    del cfg["strategy"]["position_sizing"]

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


@pytest.mark.parametrize(
    "timeframe",
    ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"],
)
def test_supported_timeframes(timeframe):
    cfg = create_valid_config()
    cfg["strategy"]["timeframe"] = timeframe

    assert StrategyValidator(ConfigManager(cfg)).validate()


def test_invalid_timeframe():
    cfg = create_valid_config()
    cfg["strategy"]["timeframe"] = "7m"

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_empty_entry_rules():
    cfg = create_valid_config()
    cfg["strategy"]["entry_rules"] = []

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_empty_exit_rules():
    cfg = create_valid_config()
    cfg["strategy"]["exit_rules"] = []

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_empty_indicators():
    cfg = create_valid_config()
    cfg["strategy"]["indicators"] = []

    with pytest.raises(ValueError):
        StrategyValidator(ConfigManager(cfg)).validate()


def test_returns_true():
    validator = StrategyValidator(ConfigManager(create_valid_config()))
    assert validator.validate() is True


def test_multiple_runs():
    validator = StrategyValidator(ConfigManager(create_valid_config()))

    assert validator.validate()
    assert validator.validate()


def test_manager_not_modified():
    manager = ConfigManager(create_valid_config())

    StrategyValidator(manager).validate()

    assert manager.has("strategy")
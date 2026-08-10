import pytest

from config.runtime_config import RuntimeConfig
from config.runtime_config_loader import RuntimeConfigLoader
from exceptions import InvalidConfigurationError


def test_loader_returns_runtime_config():
    loader = RuntimeConfigLoader()

    config = loader.load()

    assert isinstance(config, RuntimeConfig)


def test_loader_returns_default_broker():
    loader = RuntimeConfigLoader()

    config = loader.load()

    assert config.broker == "paper"


def test_loader_returns_default_mode():
    loader = RuntimeConfigLoader()

    config = loader.load()

    assert config.mode == "PAPER"


def test_loader_returns_default_portfolio():
    loader = RuntimeConfigLoader()

    config = loader.load()

    assert config.portfolio == "default"


def test_loader_returns_new_runtime_config_instance():
    loader = RuntimeConfigLoader()

    config1 = loader.load()
    config2 = loader.load()

    assert config1 is not config2


def test_loaded_config_is_valid():
    loader = RuntimeConfigLoader()

    config = loader.load()

    config.validate()


def test_multiple_loads_return_valid_configs():
    loader = RuntimeConfigLoader()

    for _ in range(5):
        loader.load().validate()


def test_loaded_config_is_runtime_config():
    loader = RuntimeConfigLoader()

    config = loader.load()

    assert type(config) is RuntimeConfig


def test_loader_can_be_reused():
    loader = RuntimeConfigLoader()

    loader.load()
    loader.load()
    loader.load()

    assert True


def test_loaded_config_defaults_match_runtime_config():
    loader = RuntimeConfigLoader()

    assert loader.load() == RuntimeConfig()


def test_loader_reads_broker_from_environment(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "dhan")

    loader = RuntimeConfigLoader()

    assert loader.load().broker == "dhan"


def test_loader_reads_mode_from_environment(monkeypatch):
    monkeypatch.setenv("TOS_MODE", "LIVE")

    loader = RuntimeConfigLoader()

    assert loader.load().mode == "LIVE"


def test_loader_reads_portfolio_from_environment(monkeypatch):
    monkeypatch.setenv("TOS_PORTFOLIO", "nifty")

    loader = RuntimeConfigLoader()

    assert loader.load().portfolio == "nifty"


def test_loader_uses_default_broker_when_missing(monkeypatch):
    monkeypatch.delenv("TOS_BROKER", raising=False)

    loader = RuntimeConfigLoader()

    assert loader.load().broker == "paper"


def test_loader_uses_default_mode_when_missing(monkeypatch):
    monkeypatch.delenv("TOS_MODE", raising=False)

    loader = RuntimeConfigLoader()

    assert loader.load().mode == "PAPER"


def test_loader_uses_default_portfolio_when_missing(monkeypatch):
    monkeypatch.delenv("TOS_PORTFOLIO", raising=False)

    loader = RuntimeConfigLoader()

    assert loader.load().portfolio == "default"


def test_loader_reads_all_environment_values(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "dhan")
    monkeypatch.setenv("TOS_MODE", "LIVE")
    monkeypatch.setenv("TOS_PORTFOLIO", "banknifty")

    config = RuntimeConfigLoader().load()

    assert config.broker == "dhan"
    assert config.mode == "LIVE"
    assert config.portfolio == "banknifty"


def test_environment_config_is_valid(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "paper")
    monkeypatch.setenv("TOS_MODE", "PAPER")

    RuntimeConfigLoader().load().validate()


def test_loader_returns_runtime_config_after_environment_load(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "paper")

    assert isinstance(RuntimeConfigLoader().load(), RuntimeConfig)


def test_environment_loading_is_repeatable(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "paper")

    loader = RuntimeConfigLoader()

    assert loader.load() == loader.load()


def test_invalid_broker_environment_raises(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "invalid")

    with pytest.raises(InvalidConfigurationError):
        RuntimeConfigLoader().load()


def test_invalid_mode_environment_raises(monkeypatch):
    monkeypatch.setenv("TOS_MODE", "INVALID")

    with pytest.raises(InvalidConfigurationError):
        RuntimeConfigLoader().load()


def test_blank_portfolio_environment_raises(monkeypatch):
    monkeypatch.setenv("TOS_PORTFOLIO", "")

    with pytest.raises(InvalidConfigurationError):
        RuntimeConfigLoader().load()


def test_whitespace_portfolio_environment_raises(monkeypatch):
    monkeypatch.setenv("TOS_PORTFOLIO", "   ")

    with pytest.raises(InvalidConfigurationError):
        RuntimeConfigLoader().load()


def test_valid_paper_environment_loads(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "paper")
    monkeypatch.setenv("TOS_MODE", "PAPER")

    RuntimeConfigLoader().load()


def test_valid_dhan_environment_loads(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "dhan")
    monkeypatch.setenv("TOS_MODE", "LIVE")

    RuntimeConfigLoader().load()


def test_default_environment_is_valid(monkeypatch):
    monkeypatch.delenv("TOS_BROKER", raising=False)
    monkeypatch.delenv("TOS_MODE", raising=False)
    monkeypatch.delenv("TOS_PORTFOLIO", raising=False)

    RuntimeConfigLoader().load()


def test_environment_validation_is_repeatable(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "paper")

    loader = RuntimeConfigLoader()

    loader.load()
    loader.load()


def test_runtime_config_loader_returns_validated_config(monkeypatch):
    monkeypatch.setenv("TOS_BROKER", "paper")

    assert RuntimeConfigLoader().load().broker == "paper"


def test_runtime_config_loader_validates_before_return(monkeypatch):
    monkeypatch.setenv("TOS_MODE", "PAPER")

    RuntimeConfigLoader().load().validate()

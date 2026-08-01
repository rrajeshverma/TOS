import pytest

from config.runtime_config import RuntimeConfig

from exceptions import InvalidConfigurationError


def test_runtime_config_defaults():
    config = RuntimeConfig()

    assert config.broker == "paper"
    assert config.mode == "PAPER"
    assert config.portfolio == "default"


def test_runtime_config_custom_values():
    config = RuntimeConfig(
        broker="dhan",
        mode="LIVE",
        portfolio="nifty",
    )

    assert config.broker == "dhan"
    assert config.mode == "LIVE"
    assert config.portfolio == "nifty"


def test_validate_raises_for_invalid_broker():
    config = RuntimeConfig(broker="invalid")

    with pytest.raises(InvalidConfigurationError):
        config.validate()


def test_validate_raises_for_invalid_mode():
    config = RuntimeConfig(mode="INVALID")

    with pytest.raises(InvalidConfigurationError):
        config.validate()


def test_validate_raises_for_blank_portfolio():
    config = RuntimeConfig(portfolio="")

    with pytest.raises(InvalidConfigurationError):
        config.validate()

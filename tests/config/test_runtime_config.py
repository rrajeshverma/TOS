from config.runtime_config import RuntimeConfig


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

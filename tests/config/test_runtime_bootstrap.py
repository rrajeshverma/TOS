import pytest

from config.runtime_bootstrap import RuntimeBootstrap


def test_bootstrap_loads_and_validates_configuration():
    bootstrap = RuntimeBootstrap()

    manager = bootstrap.load_dict(
        {
            "broker": {
                "name": "DHAN",
                "api_key": "dummy-key",
            },
            "risk": {
                "capital": 100000,
                "risk_percent": 1,
            },
            "trading": {
                "mode": "PAPER",
            },
        }
    )

    assert manager.get("broker.name") == "DHAN"
    assert manager.get("trading.mode") == "PAPER"


def test_bootstrap_rejects_invalid_configuration():
    bootstrap = RuntimeBootstrap()

    with pytest.raises(ValueError):
        bootstrap.load_dict({})

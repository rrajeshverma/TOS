import pytest

from config.config_manager import ConfigManager
from brokers.broker_validator import BrokerValidator


def create_valid_config():
    return {
        "broker": {
            "name": "DHAN",
            "api_key": "abc123",
            "client_id": "CID001",
            "access_token": "TOKEN123",
        }
    }


def test_valid_broker():
    validator = BrokerValidator(ConfigManager(create_valid_config()))
    assert validator.validate()


def test_missing_broker():
    cfg = {}
    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_missing_name():
    cfg = create_valid_config()
    del cfg["broker"]["name"]

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_missing_api_key():
    cfg = create_valid_config()
    del cfg["broker"]["api_key"]

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_missing_client_id():
    cfg = create_valid_config()
    del cfg["broker"]["client_id"]

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_missing_access_token():
    cfg = create_valid_config()
    del cfg["broker"]["access_token"]

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_empty_name():
    cfg = create_valid_config()
    cfg["broker"]["name"] = ""

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_empty_api_key():
    cfg = create_valid_config()
    cfg["broker"]["api_key"] = ""

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_empty_client_id():
    cfg = create_valid_config()
    cfg["broker"]["client_id"] = ""

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_empty_access_token():
    cfg = create_valid_config()
    cfg["broker"]["access_token"] = ""

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


@pytest.mark.parametrize(
    "broker_name",
    [
        "DHAN",
        "DELTA",
        "ZERODHA",
        "PAPER",
    ],
)
def test_supported_brokers(broker_name):
    cfg = create_valid_config()
    cfg["broker"]["name"] = broker_name

    assert BrokerValidator(ConfigManager(cfg)).validate()


def test_invalid_broker():
    cfg = create_valid_config()
    cfg["broker"]["name"] = "UNKNOWN"

    with pytest.raises(ValueError):
        BrokerValidator(ConfigManager(cfg)).validate()


def test_multiple_runs():
    validator = BrokerValidator(ConfigManager(create_valid_config()))

    assert validator.validate()
    assert validator.validate()


def test_returns_bool():
    validator = BrokerValidator(ConfigManager(create_valid_config()))

    assert validator.validate() is True


def test_manager_not_modified():
    manager = ConfigManager(create_valid_config())

    BrokerValidator(manager).validate()

    assert manager.has("broker")

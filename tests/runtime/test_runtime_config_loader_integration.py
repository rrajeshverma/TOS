from config.runtime_config import RuntimeConfig
from config.runtime_config_loader import RuntimeConfigLoader


def test_loader_returns_runtime_config_instance():
    assert isinstance(RuntimeConfigLoader().load(), RuntimeConfig)


def test_loader_default_broker():
    assert RuntimeConfigLoader().load().broker == "paper"


def test_loader_default_mode():
    assert RuntimeConfigLoader().load().mode == "PAPER"


def test_loader_default_portfolio():
    assert RuntimeConfigLoader().load().portfolio == "default"


def test_loaded_configuration_is_valid():
    RuntimeConfigLoader().load().validate()


def test_loader_returns_new_instance_each_time():
    loader = RuntimeConfigLoader()

    assert loader.load() is not loader.load()


def test_loader_can_load_multiple_times():
    loader = RuntimeConfigLoader()

    for _ in range(3):
        loader.load()


def test_loader_configuration_is_immutable():
    assert RuntimeConfigLoader().load().__dataclass_params__.frozen


def test_loader_configuration_has_slots():
    assert hasattr(RuntimeConfigLoader().load(), "__slots__")


def test_loader_produces_same_defaults(monkeypatch):
    monkeypatch.delenv("DHAN_CLIENT_ID", raising=False)
    monkeypatch.delenv("DHAN_ACCESS_TOKEN", raising=False)

    assert RuntimeConfigLoader().load() == RuntimeConfig()

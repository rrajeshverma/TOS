import pytest

from strategies.plugin_manager import PluginManager


def test_plugin_manager_starts_empty():
    manager = PluginManager()

    assert manager.plugins == []


def test_plugin_manager_can_add_plugin():
    manager = PluginManager()

    plugin = object()

    manager.register(plugin)

    assert manager.plugins == [plugin]


def test_register_none_raises():
    manager = PluginManager()

    with pytest.raises(ValueError):
        manager.register(None)

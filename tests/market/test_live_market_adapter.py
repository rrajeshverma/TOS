import pytest

from market.live_adapter import LiveMarketAdapter


def test_live_adapter_initial_status():
    adapter = LiveMarketAdapter()

    assert adapter.status() == "DISCONNECTED"


def test_live_adapter_connect():
    adapter = LiveMarketAdapter()

    adapter.connect()

    assert adapter.status() == "CONNECTED"


def test_live_adapter_disconnect():
    adapter = LiveMarketAdapter()

    adapter.connect()
    adapter.disconnect()

    assert adapter.status() == "DISCONNECTED"


def test_live_adapter_can_subscribe_symbol():
    adapter = LiveMarketAdapter()

    adapter.subscribe("NIFTY")

    assert "NIFTY" in adapter.subscriptions()


def test_live_adapter_rejects_empty_symbol():
    adapter = LiveMarketAdapter()

    with pytest.raises(ValueError):
        adapter.subscribe("")


def test_live_adapter_initial_subscriptions_empty():
    adapter = LiveMarketAdapter()

    assert adapter.subscriptions() == set()

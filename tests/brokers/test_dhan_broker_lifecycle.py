"""
Tests for Dhan broker lifecycle.
"""

from brokers.dhan_broker import DhanBroker


class MockDhanClient:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False


class MockInstrumentMapper:
    pass


def create_broker():
    return DhanBroker(
        client=MockDhanClient(),
        instrument_mapper=MockInstrumentMapper(),
    )


def test_dhan_broker_connect():
    broker = create_broker()

    broker.connect()

    assert broker.is_connected() is True


def test_dhan_broker_disconnect():
    broker = create_broker()

    broker.connect()
    broker.disconnect()

    assert broker.is_connected() is False


def test_dhan_broker_initial_state():
    broker = create_broker()

    assert broker.is_connected() is False


def test_dhan_broker_multiple_connect_is_safe():
    broker = create_broker()

    broker.connect()
    broker.connect()

    assert broker.is_connected() is True


def test_dhan_broker_multiple_disconnect_is_safe():
    broker = create_broker()

    broker.disconnect()
    broker.disconnect()

    assert broker.is_connected() is False

from unittest.mock import Mock

from brokers.dhan_broker import DhanBroker


def test_dhan_broker_has_modify_order():
    client = Mock()
    instrument_mapper = Mock()

    broker = DhanBroker(client, instrument_mapper)

    assert hasattr(broker, "modify_order")

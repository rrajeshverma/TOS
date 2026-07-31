from unittest.mock import Mock

from brokers.dhan_broker import DhanBroker


def test_cancel_order_calls_client():
    client = Mock()
    instrument_mapper = Mock()

    broker = DhanBroker(client, instrument_mapper)

    broker.cancel_order("12345")

    client.cancel_order.assert_called_once_with("12345")

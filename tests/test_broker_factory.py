import pytest

from brokers.broker_factory import BrokerFactory
from brokers.paper_broker import PaperBroker
from brokers.dhan_broker import DhanBroker


def test_create_paper_broker():
    broker = BrokerFactory.create("paper")

    assert isinstance(broker, PaperBroker)


from unittest.mock import Mock

from brokers.broker_factory import BrokerFactory
from brokers.dhan_broker import DhanBroker


def test_create_dhan_broker():
    from unittest.mock import Mock

    client = Mock()
    instrument_mapper = Mock()

    broker = BrokerFactory.create(
        "dhan",
        client,
        instrument_mapper,
    )

    assert isinstance(broker, DhanBroker)

    assert isinstance(broker, DhanBroker)


def test_invalid_broker():
    with pytest.raises(ValueError):
        BrokerFactory.create("invalid")

def test_dhan_requires_client():
    instrument_mapper = Mock()

    with pytest.raises(
        ValueError,
        match="client is required for DhanBroker",
    ):
        BrokerFactory.create(
            "dhan",
            None,
            instrument_mapper,
        )


def test_dhan_requires_instrument_mapper():
    client = Mock()

    with pytest.raises(
        ValueError,
        match="instrument_mapper is required for DhanBroker",
    ):
        BrokerFactory.create(
            "dhan",
            client,
            None,
        )

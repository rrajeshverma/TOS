import pytest

from brokers.base_broker import BaseBroker


def test_base_broker_is_abstract():
    with pytest.raises(TypeError):
        BaseBroker()


class DummyBroker(BaseBroker):
    pass


def test_incomplete_broker_cannot_be_created():
    with pytest.raises(TypeError):
        DummyBroker()

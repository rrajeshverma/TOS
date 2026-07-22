import pytest

from brokers.exceptions import (
    AuthenticationError,
    BrokerConnectionError,
    BrokerError,
    BrokerTimeoutError,
    OrderRejectedError,
)


def test_broker_error_inherits_exception():
    assert issubclass(BrokerError, Exception)


def test_connection_error_inherits_broker_error():
    assert issubclass(BrokerConnectionError, BrokerError)


def test_authentication_error_inherits_broker_error():
    assert issubclass(AuthenticationError, BrokerError)


def test_order_rejected_error_inherits_broker_error():
    assert issubclass(OrderRejectedError, BrokerError)


def test_timeout_error_inherits_broker_error():
    assert issubclass(BrokerTimeoutError, BrokerError)


def test_raise_broker_error():
    with pytest.raises(BrokerError):
        raise BrokerError("Broker error")

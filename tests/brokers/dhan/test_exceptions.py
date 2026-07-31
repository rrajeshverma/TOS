import pytest

from brokers.dhan.exceptions import (
    AuthenticationError,
    ConnectionError,
    DhanError,
    OrderError,
    WebSocketError,
)


def test_dhan_error_inherits_exception():
    error = DhanError("Something went wrong")

    assert isinstance(error, Exception)
    assert str(error) == "Something went wrong"


def test_authentication_error_inherits_dhan_error():
    error = AuthenticationError("Invalid token")

    assert isinstance(error, DhanError)


def test_connection_error_inherits_dhan_error():
    error = ConnectionError("Unable to connect")

    assert isinstance(error, DhanError)


def test_order_error_inherits_dhan_error():
    error = OrderError("Order rejected")

    assert isinstance(error, DhanError)


def test_websocket_error_inherits_dhan_error():
    error = WebSocketError("Socket closed")

    assert isinstance(error, DhanError)


@pytest.mark.parametrize(
    "exception_cls,message",
    [
        (AuthenticationError, "Auth failed"),
        (ConnectionError, "Network error"),
        (OrderError, "Rejected"),
        (WebSocketError, "Disconnected"),
    ],
)
def test_exception_message_is_preserved(exception_cls, message):
    error = exception_cls(message)

    assert str(error) == message

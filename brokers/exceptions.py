"""
Broker exception hierarchy.
"""


class BrokerError(Exception):
    """Base exception for all broker-related errors."""


class BrokerConnectionError(BrokerError):
    """Raised when broker connection fails."""


class AuthenticationError(BrokerError):
    """Raised when broker authentication fails."""


class OrderRejectedError(BrokerError):
    """Raised when an order is rejected by the broker."""


class BrokerTimeoutError(BrokerError):
    """Raised when a broker request times out."""

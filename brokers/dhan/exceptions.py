"""
Custom exceptions for the Dhan broker integration.
"""

from __future__ import annotations


class DhanError(Exception):
    """Base exception for all Dhan broker errors."""


class AuthenticationError(DhanError):
    """Raised when broker authentication fails."""


class ConnectionError(DhanError):
    """Raised when the broker connection fails."""


class OrderError(DhanError):
    """Raised when an order operation fails."""


class WebSocketError(DhanError):
    """Raised when a WebSocket operation fails."""

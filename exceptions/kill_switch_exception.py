"""
Kill switch exceptions.
"""

from exceptions.base_exception import TOSException


class KillSwitchActiveError(TOSException):
    """Raised when trading is blocked by the kill switch."""

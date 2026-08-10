"""
Base exception class for TOS.
"""


class TOSException(Exception):
    """Base class for all Trading Operating System exceptions."""


class ValidationError(TOSException):
    """Base class for validation errors."""


class MissingFieldError(ValidationError):
    """Raised when a required field is missing."""


class InvalidTimestampError(ValidationError):
    """Raised when a timestamp is invalid."""


class InvalidPriceError(ValidationError):
    """Raised when OHLC values are invalid."""


class InvalidVolumeError(ValidationError):
    """Raised when volume is invalid."""

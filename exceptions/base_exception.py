"""
Base exception class for TOS.
"""


class TOSException(Exception):
    """Base class for all Trading Operating System exceptions."""
    pass


class ValidationError(TOSException):
    """Base class for validation errors."""
    pass


class MissingFieldError(ValidationError):
    """Raised when a required field is missing."""
    pass


class InvalidTimestampError(ValidationError):
    """Raised when a timestamp is invalid."""
    pass


class InvalidPriceError(ValidationError):
    """Raised when OHLC values are invalid."""
    pass


class InvalidVolumeError(ValidationError):
    """Raised when volume is invalid."""
    pass
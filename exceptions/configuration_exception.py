"""
Configuration-related exceptions.
"""

from .base_exception import ValidationError


class ConfigurationError(ValidationError):
    """Base class for configuration errors."""


class InvalidConfigurationError(ConfigurationError):
    """Raised when runtime configuration is invalid."""


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing."""

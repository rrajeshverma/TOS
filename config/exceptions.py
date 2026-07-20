class ConfigurationError(Exception):
    """Raised when configuration is invalid."""


class ValidationError(Exception):
    """Raised when validation fails."""


class EnvironmentError(Exception):
    """Raised when environment configuration fails."""
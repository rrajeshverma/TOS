from typing import ClassVar

from config.config_manager import ConfigManager
from config.validators import (
    validate_required,
    validate_type,
)


class LoggingValidator:
    SUPPORTED_LEVELS: ClassVar[set[str]] = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }

    SUPPORTED_ROTATIONS: ClassVar[set[str]] = {
        "daily",
        "weekly",
        "monthly",
        "size",
    }

    def __init__(self, manager: ConfigManager):
        self.manager = manager

    def validate(self):
        logging = self.manager.get("logging")
        validate_required(logging)

        level = self.manager.get("logging.level")
        validate_required(level)
        validate_type(level, str)

        if level not in self.SUPPORTED_LEVELS:
            raise ValueError(f"Unsupported log level: {level}")

        directory = self.manager.get("logging.directory")
        validate_required(directory)
        validate_type(directory, str)

        filename = self.manager.get("logging.filename")
        validate_required(filename)
        validate_type(filename, str)

        rotation = self.manager.get("logging.rotation")
        validate_required(rotation)
        validate_type(rotation, str)

        if rotation not in self.SUPPORTED_ROTATIONS:
            raise ValueError(f"Unsupported rotation policy: {rotation}")

        return True

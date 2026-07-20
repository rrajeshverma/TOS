import logging
from logging.handlers import RotatingFileHandler

from logging_system.config import (
    LOG_FILE,
    LOG_LEVEL,
    ROTATING_FILE_SIZE,
    BACKUP_COUNT,
)
from logging_system.formatter import get_formatter


def get_console_handler():
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(get_formatter())
    return handler


def get_file_handler():
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=ROTATING_FILE_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )

    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(get_formatter())
    return handler

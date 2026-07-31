import logging

from logging_system.config import (
    DATE_FORMAT,
    LOG_FORMAT,
)


def get_formatter() -> logging.Formatter:
    return logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

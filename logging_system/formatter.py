import logging

from logging_system.config import (
    LOG_FORMAT,
    DATE_FORMAT,
)


def get_formatter() -> logging.Formatter:
    return logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

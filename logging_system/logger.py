import logging

from logging_system.config import LOG_LEVEL
from logging_system.handlers import (
    get_console_handler,
    get_file_handler,
)

_LOGGERS = {}


def get_logger(name: str = "TOS") -> logging.Logger:
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        logger.addHandler(get_console_handler())
        logger.addHandler(get_file_handler())
        logger.propagate = False

    _LOGGERS[name] = logger
    return logger

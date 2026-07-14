"""
=========================================================
Trading Operating System (TOS)
Module      : Logger
Version     : 1.0.0
Author      : Rajesh Varma
Description : Central logging module for TOS.
=========================================================
"""

import logging
from pathlib import Path

from config.system import LOG_DIR, LOG_LEVEL

_LOGGER_INITIALIZED = False


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    """

    global _LOGGER_INITIALIZED

    if not _LOGGER_INITIALIZED:

        log_file = Path(LOG_DIR) / "tos.log"

        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        _LOGGER_INITIALIZED = True

    return logging.getLogger(name)
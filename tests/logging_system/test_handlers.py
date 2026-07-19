import logging
from logging.handlers import RotatingFileHandler

from logging_system.config import (
    LOG_LEVEL,
    ROTATING_FILE_SIZE,
    BACKUP_COUNT,
)
from logging_system.handlers import (
    get_console_handler,
    get_file_handler,
)


def test_console_handler():
    handler = get_console_handler()

    assert isinstance(handler, logging.StreamHandler)


def test_console_handler_level():
    handler = get_console_handler()

    assert handler.level == LOG_LEVEL


def test_console_has_formatter():
    handler = get_console_handler()

    assert handler.formatter is not None


def test_file_handler():
    handler = get_file_handler()

    assert isinstance(handler, RotatingFileHandler)


def test_file_handler_level():
    handler = get_file_handler()

    assert handler.level == LOG_LEVEL


def test_file_handler_has_formatter():
    handler = get_file_handler()

    assert handler.formatter is not None


def test_backup_count():
    handler = get_file_handler()

    assert handler.backupCount == BACKUP_COUNT


def test_rotation_size():
    handler = get_file_handler()

    assert handler.maxBytes == ROTATING_FILE_SIZE


def test_console_returns_new_handler():
    assert get_console_handler() is not get_console_handler()


def test_file_returns_new_handler():
    assert get_file_handler() is not get_file_handler()


def test_console_handler_can_emit():
    handler = get_console_handler()

    record = logging.LogRecord(
        "TOS",
        logging.INFO,
        __file__,
        1,
        "Console Test",
        (),
        None,
    )

    handler.emit(record)


def test_file_handler_can_emit():
    handler = get_file_handler()

    record = logging.LogRecord(
        "TOS",
        logging.INFO,
        __file__,
        1,
        "File Test",
        (),
        None,
    )

    handler.emit(record)


def test_console_handler_name():
    handler = get_console_handler()

    assert handler.__class__.__name__ == "StreamHandler"


def test_file_handler_name():
    handler = get_file_handler()

    assert handler.__class__.__name__ == "RotatingFileHandler"


def test_handlers_are_distinct():
    assert get_console_handler() is not get_file_handler()
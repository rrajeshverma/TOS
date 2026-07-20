import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from logging_system.logger import get_logger
from logging_system.handlers import (
    get_console_handler,
    get_file_handler,
)
from logging_system.formatter import get_formatter


# ---------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------

def test_get_logger_returns_logger():
    logger = get_logger()

    assert isinstance(logger, logging.Logger)


def test_get_logger_same_instance():
    logger1 = get_logger("TOS")

    logger2 = get_logger("TOS")

    assert logger1 is logger2


def test_get_logger_different_names():
    logger1 = get_logger("ONE")

    logger2 = get_logger("TWO")

    assert logger1 is not logger2


def test_logger_name():
    logger = get_logger("MYLOGGER")

    assert logger.name == "MYLOGGER"


def test_logger_has_handlers():
    logger = get_logger("HANDLERS")

    assert len(logger.handlers) >= 2


def test_logger_not_propagating():
    logger = get_logger("NOPROP")

    assert logger.propagate is False


def test_logger_level():
    logger = get_logger("LEVEL")

    assert isinstance(logger.level, int)


# ---------------------------------------------------------------------
# Console Handler
# ---------------------------------------------------------------------

def test_console_handler_type():
    handler = get_console_handler()

    assert isinstance(handler, StreamHandler)


def test_console_handler_formatter():
    handler = get_console_handler()

    assert handler.formatter is not None


def test_console_handler_level():
    handler = get_console_handler()

    assert isinstance(handler.level, int)


# ---------------------------------------------------------------------
# File Handler
# ---------------------------------------------------------------------

def test_file_handler_type():
    handler = get_file_handler()

    assert isinstance(handler, RotatingFileHandler)


def test_file_handler_formatter():
    handler = get_file_handler()

    assert handler.formatter is not None


def test_file_handler_level():
    handler = get_file_handler()

    assert isinstance(handler.level, int)


# ---------------------------------------------------------------------
# Formatter
# ---------------------------------------------------------------------

def test_get_formatter():
    formatter = get_formatter()

    assert formatter is not None


def test_formatter_type():
    formatter = get_formatter()

    assert isinstance(formatter, logging.Formatter)


def test_formatter_formats_record():
    formatter = get_formatter()

    record = logging.LogRecord(
        name="TEST",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Hello",
        args=(),
        exc_info=None,
    )

    formatted = formatter.format(record)

    assert "Hello" in formatted


def test_formatter_multiple_records():
    formatter = get_formatter()

    for i in range(5):

        record = logging.LogRecord(
            name="TEST",
            level=logging.INFO,
            pathname=__file__,
            lineno=i,
            msg=f"Msg {i}",
            args=(),
            exc_info=None,
        )

        assert f"Msg {i}" in formatter.format(record)


def test_logger_can_log():
    logger = get_logger("WRITE")

    logger.info("Testing logger")

    assert True


def test_multiple_logger_creation():
    for i in range(10):
        logger = get_logger(f"L{i}")

        assert logger.name == f"L{i}"
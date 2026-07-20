import logging

from logging_system.config import (
    LOG_FORMAT,
    DATE_FORMAT,
)
from logging_system.formatter import get_formatter


def test_returns_formatter():
    formatter = get_formatter()

    assert isinstance(formatter, logging.Formatter)


def test_formatter_not_none():
    assert get_formatter() is not None


def test_formatter_format():
    formatter = get_formatter()

    assert formatter._style._fmt == LOG_FORMAT


def test_formatter_date_format():
    formatter = get_formatter()

    assert formatter.datefmt == DATE_FORMAT


def test_multiple_calls_return_new_objects():
    f1 = get_formatter()
    f2 = get_formatter()

    assert f1 is not f2


def test_formatter_can_format_record():
    formatter = get_formatter()

    record = logging.LogRecord(
        "TOS",
        logging.INFO,
        __file__,
        10,
        "Hello",
        (),
        None,
    )

    text = formatter.format(record)

    assert "Hello" in text


def test_format_contains_logger_name():
    formatter = get_formatter()

    record = logging.LogRecord(
        "TradingEngine",
        logging.INFO,
        __file__,
        10,
        "Started",
        (),
        None,
    )

    text = formatter.format(record)

    assert "TradingEngine" in text


def test_format_contains_level():
    formatter = get_formatter()

    record = logging.LogRecord(
        "Risk",
        logging.WARNING,
        __file__,
        10,
        "Warning",
        (),
        None,
    )

    text = formatter.format(record)

    assert "WARNING" in text


def test_error_record():
    formatter = get_formatter()

    record = logging.LogRecord(
        "Execution",
        logging.ERROR,
        __file__,
        20,
        "Failure",
        (),
        None,
    )

    assert "Failure" in formatter.format(record)


def test_debug_record():
    formatter = get_formatter()

    record = logging.LogRecord(
        "Debug",
        logging.DEBUG,
        __file__,
        20,
        "Debugging",
        (),
        None,
    )

    assert "Debugging" in formatter.format(record)


def test_info_record():
    formatter = get_formatter()

    record = logging.LogRecord(
        "Info",
        logging.INFO,
        __file__,
        20,
        "Information",
        (),
        None,
    )

    assert "Information" in formatter.format(record)


def test_formatter_reusable():
    formatter = get_formatter()

    for i in range(5):
        record = logging.LogRecord(
            "Test",
            logging.INFO,
            __file__,
            i,
            f"Message {i}",
            (),
            None,
        )

        assert formatter.format(record)


def test_returns_same_format_every_time():
    assert get_formatter()._style._fmt == get_formatter()._style._fmt


def test_formatter_handles_empty_message():
    formatter = get_formatter()

    record = logging.LogRecord(
        "Empty",
        logging.INFO,
        __file__,
        1,
        "",
        (),
        None,
    )

    assert formatter.format(record)


def test_formatter_handles_long_message():
    formatter = get_formatter()

    msg = "A" * 1000

    record = logging.LogRecord(
        "Long",
        logging.INFO,
        __file__,
        1,
        msg,
        (),
        None,
    )

    assert msg in formatter.format(record)

import logging

from logging_system.logger import get_logger


def test_returns_logger_instance():
    logger = get_logger()

    assert isinstance(logger, logging.Logger)


def test_returns_same_logger():
    logger1 = get_logger()
    logger2 = get_logger()

    assert logger1 is logger2


def test_custom_logger_name():
    logger = get_logger("MarketEngine")

    assert logger.name == "MarketEngine"


def test_same_named_logger():
    logger1 = get_logger("RiskEngine")
    logger2 = get_logger("RiskEngine")

    assert logger1 is logger2


def test_logger_has_handlers():
    logger = get_logger()

    assert len(logger.handlers) >= 2


def test_logger_level():
    logger = get_logger()

    assert logger.level == logging.INFO


def test_console_handler_exists():
    logger = get_logger()

    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)


def test_file_handler_exists():
    logger = get_logger()

    assert any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)


def test_logger_propagation_disabled():
    logger = get_logger()

    assert logger.propagate is False


def test_logging_message():
    logger = get_logger()

    logger.info("Sprint 16 logger test")


def test_warning_message():
    logger = get_logger()

    logger.warning("Warning test")


def test_error_message():
    logger = get_logger()

    logger.error("Error test")


def test_debug_message():
    logger = get_logger()

    logger.debug("Debug test")


def test_multiple_logger_names():
    market = get_logger("Market")
    risk = get_logger("Risk")

    assert market is not risk


def test_logger_name():
    logger = get_logger("TradingEngine")

    assert logger.name == "TradingEngine"


def test_logger_not_none():
    assert get_logger() is not None


def test_handlers_are_unique():
    logger = get_logger()

    ids = {id(handler) for handler in logger.handlers}

    assert len(ids) == len(logger.handlers)


def test_logger_can_log_multiple_messages():
    logger = get_logger()

    logger.info("One")
    logger.info("Two")
    logger.info("Three")


def test_default_logger_name():
    logger = get_logger()

    assert logger.name == "TOS"


def test_logger_has_formatter():
    logger = get_logger()

    for handler in logger.handlers:
        assert handler.formatter is not None

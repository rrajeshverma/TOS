import logging

from logging_system import config


def test_log_directory_exists():
    assert config.LOG_DIRECTORY.exists()


def test_log_file_name():
    assert config.LOG_FILE.name == "tos.log"


def test_log_level():
    assert config.LOG_LEVEL == logging.INFO


def test_log_format_is_string():
    assert isinstance(config.LOG_FORMAT, str)


def test_date_format_is_string():
    assert isinstance(config.DATE_FORMAT, str)


def test_backup_count_positive():
    assert config.BACKUP_COUNT > 0


def test_rotation_size_positive():
    assert config.ROTATING_FILE_SIZE > 0


def test_log_file_parent():
    assert config.LOG_FILE.parent == config.LOG_DIRECTORY


def test_directory_name():
    assert config.LOG_DIRECTORY.name == "logs"


def test_format_contains_levelname():
    assert "%(levelname)" in config.LOG_FORMAT


def test_format_contains_message():
    assert "%(message)" in config.LOG_FORMAT


def test_format_contains_name():
    assert "%(name)" in config.LOG_FORMAT


def test_date_format_not_empty():
    assert len(config.DATE_FORMAT) > 0


def test_log_file_suffix():
    assert config.LOG_FILE.suffix == ".log"


def test_log_directory_is_path():
    from pathlib import Path

    assert isinstance(config.LOG_DIRECTORY, Path)

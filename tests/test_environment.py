import os

import pytest

from config.environment import (
    get_env,
    get_bool,
    get_int,
    get_float,
)


def test_get_existing_environment_variable(monkeypatch):
    monkeypatch.setenv("BROKER", "dhan")

    assert get_env("BROKER") == "dhan"


def test_get_missing_environment_variable_returns_none():
    assert get_env("UNKNOWN") is None


def test_get_environment_variable_with_default():
    assert get_env("UNKNOWN", "paper") == "paper"


def test_get_environment_variable_empty_string(monkeypatch):
    monkeypatch.setenv("EMPTY", "")

    assert get_env("EMPTY") == ""


def test_get_environment_variable_required(monkeypatch):
    monkeypatch.setenv("API_KEY", "123")

    assert get_env("API_KEY", required=True) == "123"


def test_missing_required_environment_variable():
    with pytest.raises(ValueError):
        get_env("NOT_FOUND", required=True)


def test_get_boolean_true(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")

    assert get_bool("DEBUG") is True


def test_get_boolean_false(monkeypatch):
    monkeypatch.setenv("DEBUG", "false")

    assert get_bool("DEBUG") is False


def test_get_boolean_default():
    assert get_bool("UNKNOWN", default=True) is True


def test_get_boolean_invalid_value(monkeypatch):
    monkeypatch.setenv("DEBUG", "abc")

    with pytest.raises(ValueError):
        get_bool("DEBUG")


def test_get_integer(monkeypatch):
    monkeypatch.setenv("CAPITAL", "10000")

    assert get_int("CAPITAL") == 10000


def test_get_integer_default():
    assert get_int("UNKNOWN", default=5) == 5


def test_get_integer_invalid(monkeypatch):
    monkeypatch.setenv("CAPITAL", "abc")

    with pytest.raises(ValueError):
        get_int("CAPITAL")


def test_get_float(monkeypatch):
    monkeypatch.setenv("RISK", "2.5")

    assert get_float("RISK") == 2.5


def test_get_float_default():
    assert get_float("UNKNOWN", default=1.5) == 1.5


def test_get_float_invalid(monkeypatch):
    monkeypatch.setenv("RISK", "abc")

    with pytest.raises(ValueError):
        get_float("RISK")


def test_boolean_yes(monkeypatch):
    monkeypatch.setenv("FLAG", "yes")

    assert get_bool("FLAG") is True


def test_boolean_no(monkeypatch):
    monkeypatch.setenv("FLAG", "no")

    assert get_bool("FLAG") is False


def test_boolean_one(monkeypatch):
    monkeypatch.setenv("FLAG", "1")

    assert get_bool("FLAG") is True


def test_boolean_zero(monkeypatch):
    monkeypatch.setenv("FLAG", "0")

    assert get_bool("FLAG") is False

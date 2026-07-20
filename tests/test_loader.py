import json
import tempfile

import pytest

from config.loader import (
    load_dict,
    load_json,
    merge_configs,
)


def test_load_dictionary_returns_same_data():
    data = {"broker": "dhan"}

    assert load_dict(data) == data


def test_load_dictionary_returns_copy():
    data = {"broker": "dhan"}

    result = load_dict(data)

    assert result is not data


def test_load_empty_dictionary():
    assert load_dict({}) == {}


def test_load_dictionary_invalid_type():
    with pytest.raises(TypeError):
        load_dict([])


def test_load_json_file():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as file:
        json.dump({"broker": "dhan"}, file)
        file.flush()

        data = load_json(file.name)

        assert data["broker"] == "dhan"


def test_load_missing_json_file():
    with pytest.raises(FileNotFoundError):
        load_json("missing.json")


def test_load_invalid_json():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as file:
        file.write("{invalid json}")
        file.flush()

        with pytest.raises(ValueError):
            load_json(file.name)


def test_merge_two_configs():
    left = {"broker": "dhan"}
    right = {"capital": 10000}

    result = merge_configs(left, right)

    assert result["broker"] == "dhan"
    assert result["capital"] == 10000


def test_merge_overwrites_existing_key():
    left = {"broker": "old"}
    right = {"broker": "new"}

    result = merge_configs(left, right)

    assert result["broker"] == "new"


def test_merge_empty_configs():
    assert merge_configs({}, {}) == {}


def test_merge_nested_dictionary():
    left = {"risk": {"capital": 10000}}
    right = {"risk": {"max_loss": 500}}

    result = merge_configs(left, right)

    assert result["risk"]["capital"] == 10000
    assert result["risk"]["max_loss"] == 500


def test_merge_none_left():
    with pytest.raises(TypeError):
        merge_configs(None, {})


def test_merge_none_right():
    with pytest.raises(TypeError):
        merge_configs({}, None)


def test_load_json_returns_dictionary():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as file:
        json.dump({}, file)
        file.flush()

        assert isinstance(load_json(file.name), dict)


def test_merge_preserves_original_left():
    left = {"broker": "dhan"}

    merge_configs(left, {"capital": 100})

    assert left == {"broker": "dhan"}


def test_merge_preserves_original_right():
    right = {"capital": 100}

    merge_configs({"broker": "dhan"}, right)

    assert right == {"capital": 100}


def test_load_dictionary_nested():
    data = {"risk": {"capital": 10000}}

    result = load_dict(data)

    assert result["risk"]["capital"] == 10000


def test_merge_multiple_keys():
    left = {"a": 1}
    right = {"b": 2, "c": 3}

    result = merge_configs(left, right)

    assert len(result) == 3


def test_load_json_empty_file():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json") as file:
        file.write("{}")
        file.flush()

        assert load_json(file.name) == {}


def test_merge_returns_dictionary():
    result = merge_configs({}, {})

    assert isinstance(result, dict)
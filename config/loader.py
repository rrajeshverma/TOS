import copy
import json


def load_dict(data):
    """
    Load configuration from a dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError("Configuration must be a dictionary.")

    return copy.deepcopy(data)


def load_json(filename):
    """
    Load configuration from a JSON file.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON.") from exc


def merge_configs(left, right):
    """
    Merge two configuration dictionaries recursively.
    """
    if not isinstance(left, dict):
        raise TypeError("Left configuration must be a dictionary.")

    if not isinstance(right, dict):
        raise TypeError("Right configuration must be a dictionary.")

    result = copy.deepcopy(left)

    for key, value in right.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = copy.deepcopy(value)

    return result

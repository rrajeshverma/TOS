import os


def get_env(name, default=None, required=False):
    value = os.getenv(name, default)

    if required and value is None:
        raise ValueError(f"Environment variable '{name}' is required.")

    return value


def get_bool(name, default=None):
    value = get_env(name, default)

    if isinstance(value, bool):
        return value

    if value is None:
        return default

    value = str(value).strip().lower()

    if value in ("true", "1", "yes", "on"):
        return True

    if value in ("false", "0", "no", "off"):
        return False

    raise ValueError(f"Invalid boolean value: {value}")


def get_int(name, default=None):
    value = get_env(name, default)

    if value is None:
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid integer value: {value}")


def get_float(name, default=None):
    value = get_env(name, default)

    if value is None:
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid float value: {value}")
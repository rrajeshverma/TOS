"""
Startup Validation Checks

TOS v1.1.1
"""


def always_pass() -> bool:
    return True


def always_fail() -> bool:
    return False


def capital_check(capital: float) -> bool:
    return capital > 0


def risk_check(risk_percent: float) -> bool:
    return 0 < risk_percent <= 100


VALID_BROKERS = {
    "DHAN",
    "DELTA",
}

VALID_MODES = {
    "LIVE",
    "PAPER",
    "BACKTEST",
}


def api_key_check(api_key: str | None) -> bool:
    if api_key is None:
        return False

    return bool(api_key.strip())


def broker_name_check(name: str | None) -> bool:
    if not name:
        return False

    return name.strip().upper() in VALID_BROKERS


def trading_mode_check(mode: str | None) -> bool:
    if not mode:
        return False

    return mode.strip().upper() in VALID_MODES

from __future__ import annotations

from datetime import UTC, datetime
from itertools import count
from threading import Lock

_lock = Lock()
_counter = count(1)


def _generate(prefix: str) -> str:
    """
    Generate a unique identifier.

    Format:
        PREFIX + YYYYMMDD + 4-digit sequence

    Example:
        D202607140001
    """
    with _lock:
        sequence = next(_counter)

    return f"{prefix}{datetime.now(UTC):%Y%m%d}{sequence:04d}"


def generate_decision_id() -> str:
    return _generate("D")


def generate_trade_id() -> str:
    return _generate("T")


def generate_order_id() -> str:
    return _generate("O")


def generate_position_id() -> str:
    return _generate("P")

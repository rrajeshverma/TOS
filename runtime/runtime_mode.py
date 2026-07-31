from __future__ import annotations

from enum import StrEnum


class RuntimeMode(StrEnum):
    VERSION = "version"
    HEALTH = "health"
    VALIDATE = "validate"
    PAPER = "paper"
    LIVE = "live"
    REPLAY = "replay"
    BACKTEST = "backtest"

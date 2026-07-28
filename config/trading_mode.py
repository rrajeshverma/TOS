"""
TOS Trading Mode Configuration

Loads execution mode from environment.

Supported:
- PAPER
- LIVE
"""

from __future__ import annotations

import os

from trading.execution_mode import ExecutionMode


DEFAULT_MODE = ExecutionMode.PAPER.value


def get_trading_mode() -> ExecutionMode:
    """
    Return configured trading mode.

    Defaults to PAPER for safety.
    """

    mode = os.getenv(
        "TOS_MODE",
        DEFAULT_MODE,
    ).upper()


    if mode == ExecutionMode.LIVE.value:
        return ExecutionMode.LIVE


    return ExecutionMode.PAPER

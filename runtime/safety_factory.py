"""
Runtime safety factory.
"""

from __future__ import annotations

from safety.composite_execution_guard import CompositeExecutionGuard
from safety.kill_switch import KillSwitch
from safety.kill_switch_guard import KillSwitchGuard
from safety.market_hours_guard import MarketHoursGuard
from safety.trade_limit_guard import TradeLimitGuard
from trading.execution_mode import ExecutionMode, ExecutionModeGuard


class SafetyFactory:
    """Creates the default execution guard stack."""

    @staticmethod
    def create(
        mode: ExecutionMode = ExecutionMode.PAPER,
    ) -> CompositeExecutionGuard:
        """Build the production execution guard."""

        return CompositeExecutionGuard(
            [
                ExecutionModeGuard(mode),
                KillSwitchGuard(KillSwitch()),
                MarketHoursGuard(),
                TradeLimitGuard(),
            ]
        )

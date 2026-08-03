"""
Runtime health monitor.
"""

from dataclasses import dataclass

from runtime.session_state import SessionState
from shared.runtime_status import RuntimeStatus


@dataclass(slots=True, frozen=True)
class RuntimeHealth:
    """Trading runtime health."""

    runtime_status: RuntimeStatus
    session_state: SessionState
    broker_connected: bool
    market_data_connected: bool
    trading_allowed: bool

"""
Trading session states.
"""

from enum import StrEnum


class SessionState(StrEnum):
    """Trading session."""

    PRE_OPEN = "PRE_OPEN"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    HOLIDAY = "HOLIDAY"
    MAINTENANCE = "MAINTENANCE"

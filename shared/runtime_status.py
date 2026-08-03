"""
Trading Runtime States
"""

from enum import StrEnum


class RuntimeStatus(StrEnum):
    """Lifecycle of the Trading Runtime."""

    INITIALIZING = "INITIALIZING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"

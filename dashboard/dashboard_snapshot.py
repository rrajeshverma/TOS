"""
Dashboard snapshot models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RuntimeSnapshot:
    """
    Runtime snapshot for dashboard rendering.
    """

    status: str
    mode: str
    running: bool
    metrics: dict[str, int]

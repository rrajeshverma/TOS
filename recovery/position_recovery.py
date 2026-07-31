"""
TOS Position Recovery Service

Restores position state after runtime restart.
"""

from __future__ import annotations


class PositionRecoveryService:
    """
    Handles recovery of broker positions.
    """

    def __init__(self) -> None:
        self._positions: dict[str, dict] = {}

    def recover(
        self,
        position: dict,
    ) -> dict:
        """
        Recover a broker position.
        """

        symbol = position.get("symbol")

        if symbol is None:
            raise ValueError("Position symbol required")

        self._positions[symbol] = position

        return position

    def get(
        self,
        symbol: str,
    ) -> dict | None:
        """
        Return recovered position.
        """

        return self._positions.get(symbol)

    def all_positions(
        self,
    ) -> list[dict]:
        """
        Return all recovered positions.
        """

        return list(self._positions.values())

    def count(self) -> int:
        """
        Return recovered position count.
        """

        return len(self._positions)

    def clear(self) -> None:
        """
        Clear recovery state.
        """

        self._positions.clear()

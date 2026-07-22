"""
=========================================================
Trading Operating System (TOS)

Module      : Position Book
Description : Maintains active trading positions.
=========================================================
"""

from __future__ import annotations


class PositionBook:
    """
    Stores and manages active positions.

    PositionManager manages one position lifecycle.
    PositionBook manages the collection of positions.
    """

    def __init__(self):
        self._positions = {}

    def add_position(
        self,
        position_id,
        position,
    ):
        """
        Add or update a position.
        """
        self._positions[position_id] = position

    def get_position(
        self,
        position_id,
    ):
        """
        Retrieve position by id.
        """
        return self._positions.get(position_id)

    def get_all_positions(self):
        """
        Return all active positions.
        """
        return list(self._positions.values())

    def contains(
        self,
        position_id,
    ):
        """
        Check whether position exists.
        """
        return position_id in self._positions

    def remove_position(
        self,
        position_id,
    ):
        """
        Remove position safely.
        """
        self._positions.pop(
            position_id,
            None,
        )

    def count(self):
        """
        Return active position count.
        """
        return len(self._positions)

    def clear(self):
        """
        Remove all positions.
        """
        self._positions.clear()
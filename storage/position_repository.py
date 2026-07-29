from __future__ import annotations

from domain.position import Position


class PositionRepository:
    """
    In-memory repository for Position objects.
    """

    def __init__(self) -> None:
        self._positions: dict[str, Position] = {}

    def save(
        self,
        position: Position,
    ) -> None:
        self._positions[position.position_id] = position

    def get(
        self,
        position_id: str,
    ) -> Position | None:
        return self._positions.get(position_id)

    def delete(
        self,
        position_id: str,
    ) -> None:
        self._positions.pop(position_id, None)

    def exists(
        self,
        position_id: str,
    ) -> bool:
        return position_id in self._positions

    def all(self) -> list[Position]:
        return list(self._positions.values())

    def count(self) -> int:
        return len(self._positions)

    def clear(self) -> None:
        self._positions.clear()

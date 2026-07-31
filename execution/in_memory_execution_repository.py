from __future__ import annotations

from execution.execution_repository import (
    ExecutionRepository,
)


class InMemoryExecutionRepository(
    ExecutionRepository,
):
    def __init__(self) -> None:
        self._storage = {}

    def save(
        self,
        order_id: str,
        data,
    ) -> None:
        self._storage[order_id] = data

    def load(
        self,
        order_id: str,
    ):
        return self._storage.get(order_id)

    def exists(
        self,
        order_id: str,
    ) -> bool:
        return order_id in self._storage

    def delete(
        self,
        order_id: str,
    ) -> None:
        self._storage.pop(
            order_id,
            None,
        )

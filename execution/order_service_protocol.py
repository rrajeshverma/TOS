from __future__ import annotations

from typing import Protocol


class OrderServiceProtocol(Protocol):
    def submit(self, request) -> str: ...

    def place_order(self, request) -> dict: ...

    def register_broker_order(
        self,
        order_id: str,
        broker_order_id: str,
    ) -> None: ...

    def update_status(
        self,
        order_id: str,
        status,
    ) -> None: ...

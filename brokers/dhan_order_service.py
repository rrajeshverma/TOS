from __future__ import annotations

from brokers.clients.dhan_client import DhanClient
from execution.order_service_protocol import OrderServiceProtocol


class DhanOrderService(OrderServiceProtocol):
    """Adapter between ExecutionEngine and DhanClient."""

    def __init__(self, client: DhanClient) -> None:
        self.client = client
        self._order_map = {}
        self._orders = {}
        self._fills = {}

    # -----------------------------------
    # MAIN ENTRY (used by executor)
    # -----------------------------------
    def submit(self, request) -> str:
        res = self.place_order(
            security_id=request.security_id,
            exchange_segment=request.exchange_segment,
            transaction_type=request.side,
            quantity=request.quantity,
            price=request.price,
        )

        if "orderId" not in res:
            raise Exception(f"Dhan order failed: {res}")

        broker_order_id = res["orderId"]

        # store mapping
        self._order_map[request.order_id] = broker_order_id
        self._orders[request.order_id] = request
        self._fills[request.order_id] = 0

        return request.order_id

    # -----------------------------------
    # 🔥 FIXED: moved OUTSIDE submit()
    # -----------------------------------
    def get_internal_order(self, order_id):
        return self._orders.get(order_id)

    # -----------------------------------
    # EXISTING METHODS (KEEP)
    # -----------------------------------
    def get_positions(self):
        return self.client.get_positions()

    def get_orders(self):
        return self.client.get_orders()

    def get_holdings(self):
        return self.client.get_holdings()

    def get_fund_limits(self):
        return self.client.get_fund_limits()

    def get_order(self, order_id):
        return self.client.get_order(order_id)

    # -----------------------------------
    # PLACE ORDER (ADAPT)
    # -----------------------------------
    def place_order(self, **kwargs):
        return self.client.place_order(**kwargs)

    def modify_order(self, order_id, **kwargs):
        return self.client.modify_order(order_id, **kwargs)

    def cancel_order(self, order_id):
        return self.client.cancel_order(order_id)

    # -----------------------------------
    # PROTOCOL REQUIRED METHODS
    # -----------------------------------
    def register_broker_order(
        self,
        order_id: str,
        broker_order_id: str,
    ) -> None:
        self._order_map[order_id] = broker_order_id

    def update_status(
        self,
        order_id: str,
        status,
    ) -> None:
        print(f"[STATUS] {order_id} -> {status}")

    # -----------------------------------
    # HELPER
    # -----------------------------------
    def sync_order_status(self, order_id: str):
        broker_order_id = self._order_map.get(order_id)

        if not broker_order_id:
            raise ValueError(f"No broker order for {order_id}")

        res = self.client.get_order_status(broker_order_id)[0]

        self.update_status(order_id, res["orderStatus"])

        return res

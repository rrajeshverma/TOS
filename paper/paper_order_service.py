import random
import time
from uuid import uuid4


class InternalOrder:
    def __init__(self, request):
        self.symbol = request.get("symbol")
        self.quantity = request.get("qty") or request.get("quantity", 1)
        self.side = request.get("side")


class PaperOrderService:
    def __init__(self):
        self.orders = {}
        self._orders = self.orders
        self._fills = {}

    # -------------------------------
    # SUBMIT ORDER
    # -------------------------------
    def submit(self, request):
        if request is None:
            raise ValueError("request cannot be None")

        order_id = f"PAPER-{uuid4().hex[:8]}"

        quantity = request.get("qty") or request.get("quantity", 1)

        self.orders[order_id] = {
            "symbol": request["symbol"],
            "side": request["side"],
            "quantity": quantity,
            "request": dict(request),
            "status": "OPEN",
            "filled_qty": 0,
            "total_qty": quantity,
            "price": request["price"],
            "created_at": time.time(),
        }

        self._fills[order_id] = 0

        return order_id

    # -------------------------------
    # SIMULATED ORDER STATUS
    # -------------------------------
    def get_order_status(self, order_id):
        order = self.orders.get(order_id)

        if not order:
            return None

        elapsed = time.time() - order["created_at"]

        # Simulate delay before fill starts
        if elapsed < 2:
            return self._format(order)

        # Simulate partial fills
        if order["filled_qty"] < order["total_qty"]:
            fill_step = random.randint(1, order["total_qty"])
            order["filled_qty"] = min(
                order["filled_qty"] + fill_step,
                order["total_qty"],
            )

            if order["filled_qty"] < order["total_qty"]:
                order["status"] = "PARTIAL"
            else:
                order["status"] = "TRADED"

        return self._format(order)

    # -------------------------------
    # FORMAT RESPONSE (LIKE BROKER)
    # -------------------------------
    def _format(self, order):
        return {
            "orderStatus": order["status"],
            "filledQty": order["filled_qty"],
            "averageTradedPrice": order["price"],
        }

    # -------------------------------
    # HELPERS
    # -------------------------------
    def get_order_map(self):
        return {oid: oid for oid in self.orders.keys()}

    def remove_order(self, order_id):
        self.orders.pop(order_id, None)
        self._fills.pop(order_id, None)

    def get_internal_order(self, order_id):
        order = self.orders.get(order_id)

        if not order:
            return None

        return InternalOrder(order["request"])

from dataclasses import dataclass, field


@dataclass
class OrderRecovery:
    pending_orders: dict = field(default_factory=dict)

    def add_order(self, order_id, symbol):
        self.pending_orders[order_id] = symbol

    def remove_order(self, order_id):
        self.pending_orders.pop(order_id, None)

    def has_pending_orders(self):
        return len(self.pending_orders) > 0

    def pending_count(self):
        return len(self.pending_orders)

    def clear(self):
        self.pending_orders.clear()

    def get_order(self, order_id):
        return self.pending_orders.get(order_id)

    def summary(self):
        return {
            "pending_orders": self.pending_orders.copy(),
            "pending_count": self.pending_count(),
            "has_pending": self.has_pending_orders(),
        }

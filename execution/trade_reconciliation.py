from dataclasses import dataclass, field


@dataclass
class TradeReconciliation:
    local_trades: dict = field(default_factory=dict)
    broker_trades: dict = field(default_factory=dict)

    def add_local(self, trade_id, quantity):
        self.local_trades[trade_id] = quantity

    def add_broker(self, trade_id, quantity):
        self.broker_trades[trade_id] = quantity

    def remove_local(self, trade_id):
        self.local_trades.pop(trade_id, None)

    def remove_broker(self, trade_id):
        self.broker_trades.pop(trade_id, None)

    def difference(self, trade_id):
        return self.local_trades.get(trade_id, 0) - self.broker_trades.get(trade_id, 0)

    def is_reconciled(self):
        return self.local_trades == self.broker_trades

    def reset(self):
        self.local_trades.clear()
        self.broker_trades.clear()

    def summary(self):
        return {
            "local_trades": self.local_trades.copy(),
            "broker_trades": self.broker_trades.copy(),
            "reconciled": self.is_reconciled(),
        }

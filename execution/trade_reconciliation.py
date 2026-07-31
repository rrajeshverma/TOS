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

    def missing_broker_trades(self):
        """
        Trades present locally but missing at broker.
        """

        return [
            trade_id
            for trade_id in self.local_trades
            if trade_id not in self.broker_trades
        ]

    def extra_broker_trades(self):
        """
        Trades present at broker but missing locally.
        """

        return [
            trade_id
            for trade_id in self.broker_trades
            if trade_id not in self.local_trades
        ]

    def reconciliation_report(self):
        """
        Complete reconciliation report.
        """

        differences = {}

        for trade_id in set(self.local_trades) & set(self.broker_trades):
            difference = self.difference(trade_id)

            if difference != 0:
                differences[trade_id] = difference

        return {
            "reconciled": self.is_reconciled(),
            "missing": self.missing_broker_trades(),
            "extra": self.extra_broker_trades(),
            "differences": differences,
        }

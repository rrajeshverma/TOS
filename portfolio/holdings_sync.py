from dataclasses import dataclass, field
from typing import Any


@dataclass
class HoldingsSync:
    broker: Any | None = None
    local_holdings: dict = field(default_factory=dict)
    broker_holdings: dict = field(default_factory=dict)

    def set_local(self, symbol, quantity):
        self.local_holdings[symbol] = quantity

    def set_broker(self, symbol, quantity):
        self.broker_holdings[symbol] = quantity

    def remove_local(self, symbol):
        self.local_holdings.pop(symbol, None)

    def remove_broker(self, symbol):
        self.broker_holdings.pop(symbol, None)

    def difference(self, symbol):
        return self.local_holdings.get(symbol, 0) - self.broker_holdings.get(symbol, 0)

    def is_in_sync(self):
        return self.local_holdings == self.broker_holdings

    def reset(self):
        self.local_holdings.clear()
        self.broker_holdings.clear()

    def summary(self):
        return {
            "local_holdings": self.local_holdings.copy(),
            "broker_holdings": self.broker_holdings.copy(),
            "in_sync": self.is_in_sync(),
        }

    def sync(self):
        if self.broker is None:
            raise RuntimeError("Broker is not configured.")

        holdings = self.broker.get_holdings()

        if isinstance(holdings, list):
            self.broker_holdings.clear()

            for holding in holdings:
                if (
                    isinstance(holding, dict)
                    and "securityId" in holding
                    and "quantity" in holding
                ):
                    self.broker_holdings[holding["securityId"]] = holding["quantity"]

        return holdings

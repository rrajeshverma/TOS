from dataclasses import dataclass, field
from typing import Any


@dataclass
class AccountSync:
    broker: Any | None = None
    account_data: dict = field(default_factory=dict)

    def sync(self):
        if self.broker is None:
            raise RuntimeError("Broker is not configured.")

        self.account_data = self.broker.get_funds()
        return self.account_data

    def reset(self):
        self.account_data.clear()

    def summary(self):
        return self.account_data.copy()

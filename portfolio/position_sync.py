from dataclasses import dataclass, field
from typing import Any


@dataclass
class PositionSync:
    broker: Any | None = None
    local_positions: dict = field(default_factory=dict)
    broker_positions: dict = field(default_factory=dict)

    def set_local(self, symbol, quantity):
        self.local_positions[symbol] = quantity

    def set_broker(self, symbol, quantity):
        self.broker_positions[symbol] = quantity

    def remove_local(self, symbol):
        self.local_positions.pop(symbol, None)

    def remove_broker(self, symbol):
        self.broker_positions.pop(symbol, None)

    def difference(self, symbol):
        return self.local_positions.get(symbol, 0) - self.broker_positions.get(
            symbol, 0
        )

    def is_in_sync(self):
        return self.local_positions == self.broker_positions

    def reset(self):
        self.local_positions.clear()
        self.broker_positions.clear()

    def summary(self):
        return {
            "local_positions": self.local_positions.copy(),
            "broker_positions": self.broker_positions.copy(),
            "in_sync": self.is_in_sync(),
        }

    def sync(self):
        """
        Retrieve live positions from the configured broker.
        """
        if self.broker is None:
            raise RuntimeError("Broker is not configured.")

        positions = self.broker.get_positions()

        # Optional: populate broker_positions if the broker returns
        # dictionaries with securityId and quantity.
        if isinstance(positions, list):
            self.broker_positions.clear()

            for position in positions:
                if (
                    isinstance(position, dict)
                    and "securityId" in position
                    and "quantity" in position
                ):
                    self.broker_positions[position["securityId"]] = position["quantity"]

        return positions

    def missing_broker_positions(self):
        """
        Positions available locally but missing at broker.
        """

        return [
            symbol
            for symbol in self.local_positions
            if symbol not in self.broker_positions
        ]

    def extra_broker_positions(self):
        """
        Positions available at broker but missing locally.
        """

        return [
            symbol
            for symbol in self.broker_positions
            if symbol not in self.local_positions
        ]

    def sync_report(self):
        """
        Complete position synchronization report.
        """

        differences = {}

        for symbol in set(self.local_positions) & set(self.broker_positions):
            difference = self.difference(symbol)

            if difference != 0:
                differences[symbol] = difference

        return {
            "in_sync": self.is_in_sync(),
            "missing": self.missing_broker_positions(),
            "extra": self.extra_broker_positions(),
            "differences": differences,
        }

from dataclasses import dataclass, field


@dataclass
class PositionSync:
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
        return (
            self.local_positions.get(symbol, 0)
            - self.broker_positions.get(symbol, 0)
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
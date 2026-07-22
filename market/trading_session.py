from dataclasses import dataclass
from datetime import time


@dataclass
class TradingSession:
    entry_start: time = time(9, 45)
    last_entry: time = time(14, 45)
    force_exit: time = time(15, 15)
    market_open: time = time(9, 15)
    market_close: time = time(15, 30)

    def is_entry_allowed(self, current_time: time) -> bool:
        return self.entry_start <= current_time <= self.last_entry

    def is_force_exit(self, current_time: time) -> bool:
        return current_time >= self.force_exit

    def is_market_open(self, current_time: time) -> bool:
        return self.market_open <= current_time <= self.market_close

    def summary(self):
        return {
            "entry_start": self.entry_start,
            "last_entry": self.last_entry,
            "force_exit": self.force_exit,
            "market_open": self.market_open,
            "market_close": self.market_close,
        }

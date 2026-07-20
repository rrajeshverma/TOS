from dataclasses import dataclass


@dataclass
class CircuitBreaker:
    max_consecutive_losses: int = 3
    max_daily_loss: float = 10000

    consecutive_losses: int = 0
    daily_loss: float = 0

    def record_loss(self, amount):
        self.daily_loss += amount
        self.consecutive_losses += 1

    def record_profit(self, amount):
        self.consecutive_losses = 0

    def is_tripped(self):
        return (
            self.consecutive_losses >= self.max_consecutive_losses
            or self.daily_loss >= self.max_daily_loss
        )

    def reset(self):
        self.daily_loss = 0
        self.consecutive_losses = 0

    def summary(self):
        return {
            "daily_loss": self.daily_loss,
            "consecutive_losses": self.consecutive_losses,
            "tripped": self.is_tripped(),
        }
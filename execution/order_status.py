from dataclasses import dataclass


@dataclass
class OrderStatus:
    state: str = "NEW"

    def mark_submitted(self):
        self.state = "SUBMITTED"

    def mark_filled(self):
        self.state = "FILLED"

    def mark_cancelled(self):
        self.state = "CANCELLED"

    def mark_rejected(self):
        self.state = "REJECTED"

    def is_open(self):
        return self.state in ("NEW", "SUBMITTED")

    def is_closed(self):
        return self.state == "FILLED"

    def is_cancelled(self):
        return self.state == "CANCELLED"

    def is_rejected(self):
        return self.state == "REJECTED"

    def reset(self):
        self.state = "NEW"

    def to_dict(self):
        return {"state": self.state}

    def __str__(self):
        return self.state

    def __repr__(self):
        return f"OrderStatus(state='{self.state}')"
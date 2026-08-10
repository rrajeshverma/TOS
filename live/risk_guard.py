class RiskGuard:
    """
    Controls trading risk limits.
    """

    def __init__(
        self,
        daily_loss_limit=0,
        max_positions=1,
    ):
        self.daily_loss_limit = daily_loss_limit
        self.max_positions = max_positions

        self.daily_loss = 0
        self.positions = 0
        self._blocked = False

    def record_loss(
        self,
        amount,
    ):
        self.daily_loss += amount

    def add_position(self):
        self.positions += 1

    def can_open_position(self):
        return self.positions < self.max_positions

    def block(self):
        self._blocked = True

    def allow(self):
        self._blocked = False

    def can_trade(self):
        if self._blocked:
            return False

        return not (self.daily_loss_limit > 0 and self.daily_loss >= self.daily_loss_limit)

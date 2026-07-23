class PortfolioRisk:
    def __init__(self, capital, risk_percent):
        self.capital = capital
        self.risk_percent = risk_percent
        self.current_risk = 0
        self.daily_loss = 0

    # --------------------------------------------------
    # Risk Limits
    # --------------------------------------------------

    def maximum_risk(self):
        return self.capital * self.risk_percent / 100

    def remaining_risk(self):
        return max(0, self.maximum_risk() - self.current_risk)

    # --------------------------------------------------
    # Daily Loss
    # --------------------------------------------------

    def remaining_daily_loss(self):
        return max(0, self.maximum_risk() - self.daily_loss)

    # --------------------------------------------------
    # Exposure
    # --------------------------------------------------

    def exposure_percent(self):
        maximum = self.maximum_risk()

        if maximum == 0:
            return 0.0

        return (self.current_risk / maximum) * 100

    def can_open_position(self):
        return self.remaining_risk() > 0

        # --------------------------------------------------

    # Snapshot Integration
    # --------------------------------------------------

    def update_from_snapshot(
        self,
        snapshot,
    ):
        """
        Update current risk from portfolio snapshot.

        Losses increase risk exposure.
        Profits do not create risk.
        """

        total_pnl = snapshot.realized_pnl + snapshot.unrealized_pnl

        self.current_risk = max(
            0,
            -total_pnl,
        )

        return self.current_risk

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):
        return {
            "maximum_risk": self.maximum_risk(),
            "remaining_risk": self.remaining_risk(),
            "daily_loss": self.daily_loss,
            "remaining_daily_loss": self.remaining_daily_loss(),
            "exposure_percent": self.exposure_percent(),
            "can_open_position": self.can_open_position(),
        }

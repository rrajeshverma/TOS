"""
Risk Dashboard Widget.
"""


class RiskWidget:
    """
    Displays runtime risk information.
    """

    def __init__(
        self,
        status="SAFE",
        daily_loss=0.0,
        kill_switch=False,
        circuit_breaker=False,
    ) -> None:
        self.status = status
        self.daily_loss = daily_loss
        self.kill_switch = kill_switch
        self.circuit_breaker = circuit_breaker

    def render(self) -> str:
        """
        Render risk information.
        """

        return (
            "Risk\n"
            f"Status            : {self.status}\n"
            f"Daily Loss        : ₹{self.daily_loss:,.2f}\n"
            f"Kill Switch       : {'ON' if self.kill_switch else 'OFF'}\n"
            f"Circuit Breaker   : {'ON' if self.circuit_breaker else 'OFF'}\n"
        )

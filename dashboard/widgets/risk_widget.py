"""
Risk Dashboard Widget.
"""

from dataclasses import dataclass


@dataclass
class RiskWidget:
    """
    Displays runtime risk information.
    """

    status: str = "SAFE"
    daily_loss: float = 0.0
    kill_switch: bool = False
    circuit_breaker: bool = False

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

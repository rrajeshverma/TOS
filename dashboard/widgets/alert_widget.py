"""
Alert Dashboard Widget.
"""


class AlertWidget:
    """
    Displays runtime alerts.
    """

    def __init__(self, alerts=None) -> None:
        self.alerts = alerts or []

    def render(self) -> str:
        """
        Render alerts.
        """

        if not self.alerts:
            return "Alerts\nNone\n"

        return "Alerts\n" + "\n".join(
            f"- {alert}"
            for alert in self.alerts
        ) + "\n"

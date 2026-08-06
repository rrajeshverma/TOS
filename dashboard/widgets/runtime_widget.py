"""
Runtime Dashboard Widget.
"""


class RuntimeWidget:
    """
    Displays runtime information.
    """

    def __init__(
        self,
        status="STOPPED",
        mode="PAPER",
        uptime="00:00:00",
    ) -> None:
        self.status = status
        self.mode = mode
        self.uptime = uptime

    def render(self) -> str:
        """
        Render runtime information.
        """

        return (
            "Runtime\n"
            f"Status : {self.status}\n"
            f"Mode   : {self.mode}\n"
            f"Uptime : {self.uptime}\n"
        )

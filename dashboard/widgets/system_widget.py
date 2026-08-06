"""
System Dashboard Widget.
"""


class SystemWidget:
    """
    Displays system resource usage.
    """

    def __init__(
        self,
        cpu=0.0,
        memory=0.0,
        uptime="00:00:00",
    ) -> None:
        self.cpu = cpu
        self.memory = memory
        self.uptime = uptime

    def render(self) -> str:
        """
        Render system information.
        """

        return (
            "System\n"
            f"CPU      : {self.cpu:.1f}%\n"
            f"Memory   : {self.memory:.1f} MB\n"
            f"Uptime   : {self.uptime}\n"
        )

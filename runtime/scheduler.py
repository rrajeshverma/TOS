"""
Simple task scheduler.
"""


class Scheduler:
    """Executes scheduled tasks."""

    def __init__(self, interval: int = 1) -> None:
        self.interval = interval

    def run(self, task) -> None:
        task()
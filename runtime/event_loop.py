"""
Runtime event loop.
"""


class EventLoop:
    """Simple execution loop."""

    def __init__(self) -> None:
        self.running = False
        self.iterations = 0

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    def run_iteration(self) -> None:
        self.iterations += 1

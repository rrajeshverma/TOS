"""
Application runtime entry point.
"""


class Application:
    """Main application runtime."""

    def __init__(self) -> None:
        self.services: dict = {}
        self.config: dict = {}
        self.running: bool = False

    def load_configuration(self, config: dict) -> None:
        self.config.update(config)

    def start(self) -> None:
        self.running = True

    def shutdown(self) -> None:
        self.running = False

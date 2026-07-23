"""
Application startup manager.
"""


class Startup:
    """Handles application startup."""

    def __init__(self) -> None:
        self.broker = None
        self.portfolio = None
        self.services_initialized = False

    def load_broker(self, broker: str) -> None:
        self.broker = broker

    def load_portfolio(self, portfolio: str) -> None:
        self.portfolio = portfolio

    def initialize_services(self) -> None:
        self.services_initialized = True

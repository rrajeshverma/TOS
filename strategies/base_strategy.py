"""
TOS Strategy Plugin Framework

Base contract for all trading strategies.
"""


class BaseStrategy:
    """
    Abstract strategy interface.

    Every strategy must implement:
    - name()
    - analyze()
    - generate_signal()
    """

    def name(self):
        raise NotImplementedError(
            "Strategy name must be implemented"
        )

    def analyze(
        self,
        market,
    ):
        raise NotImplementedError(
            "Strategy analyze must be implemented"
        )

    def generate_signal(
        self,
        market,
    ):
        raise NotImplementedError(
            "Strategy signal generation must be implemented"
        )

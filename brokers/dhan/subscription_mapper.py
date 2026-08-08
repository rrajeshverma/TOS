"""
Dhan Subscription Mapper
Converts internal symbols to Dhan subscription format
"""


class DhanSubscriptionMapper:
    """
    Convert internal symbol → Dhan subscription tuple
    """

    @staticmethod
    def map(symbol: str) -> tuple:
        """
        Returns tuple in format expected by Dhan:
        (Exchange, Symbol, Type)
        """
        return ("NSE", symbol, "Ticker")

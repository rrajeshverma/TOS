from dhanhq import dhanhq, DhanContext

from config.system import (
    DHAN_CLIENT_ID,
    DHAN_ACCESS_TOKEN,
)


class DhanClient:
    """
    Thin wrapper around the official Dhan SDK.
    """

    def __init__(self):
        self._context = DhanContext(
            DHAN_CLIENT_ID,
            DHAN_ACCESS_TOKEN,
        )

        self._sdk = dhanhq(self._context)

    @property
    def sdk(self):
        return self._sdk

    def get_fund_limits(self):
        return self._sdk.get_fund_limits()

    def get_positions(self):
        return self._sdk.get_positions()

    def get_holdings(self):
        return self._sdk.get_holdings()

    def get_orders(self):
        return self._sdk.get_order_list()
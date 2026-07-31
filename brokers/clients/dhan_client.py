from dhanhq import DhanContext, dhanhq

from config.system import (
    DHAN_ACCESS_TOKEN,
    DHAN_CLIENT_ID,
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
        self.connected = False

    @property
    def sdk(self):
        return self._sdk

    # -----------------------------------------------------
    # Connection
    # -----------------------------------------------------

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def is_connected(self):
        return self.connected

    # -----------------------------------------------------
    # Account
    # -----------------------------------------------------

    def get_fund_limits(self):
        return self._sdk.get_fund_limits()

    def get_positions(self):
        return self._sdk.get_positions()

    def get_holdings(self):
        return self._sdk.get_holdings()

    # -----------------------------------------------------
    # Orders
    # -----------------------------------------------------

    def get_order_list(self):
        return self._sdk.get_order_list()

    def get_orders(self):
        """
        Backward-compatible alias.
        """
        return self.get_order_list()

    def get_order(self, order_id):
        return self._sdk.get_order_by_id(order_id)

    def place_order(self, **kwargs):
        return self._sdk.place_order(**kwargs)

    def modify_order(self, order_id, **kwargs):
        return self._sdk.modify_order(
            order_id=order_id,
            **kwargs,
        )

    def cancel_order(self, order_id):
        return self._sdk.cancel_order(order_id)

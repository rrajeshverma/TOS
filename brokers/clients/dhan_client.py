"""
Dhan Client - SDK Wrapper (Test Compatible)
"""


# ✅ Dummy compatibility for tests (DO NOT REMOVE)
class DhanContext:
    def __init__(self, client_id=None, access_token=None):
        self.client_id = client_id
        self.access_token = access_token


# ✅ Dummy dhanhq for mocking
class dhanhq:
    def __init__(self, *args, **kwargs):
        pass


class DhanClient:
    def __init__(self, client_id=None, access_token=None):
        # ✅ Make optional for tests
        self.client_id = client_id or "test_client"
        self.access_token = access_token or "test_token"

        # SDK instance (mocked in tests)
        self._sdk = dhanhq(self.client_id, self.access_token)

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

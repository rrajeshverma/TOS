from dhanhq import dhanhq


class DhanDataProvider:
    def __init__(self, client_id: str, access_token: str):
        self.client = dhanhq(client_id, access_token)

    def get_ltp(self, exchange: str, security_id: str):
        try:
            return self.client.get_ltp_data(exchange, security_id)
        except Exception as e:
            print("Error fetching LTP:", e)
            return None

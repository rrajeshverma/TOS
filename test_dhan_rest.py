import time

from dhanhq import dhanhq


# 🔥 SAME CONTEXT
class DhanContext:
    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token

    def get_client_id(self):
        return self.client_id

    def get_access_token(self):
        return self.access_token

    def get_dhan_http(self):
        class DhanHTTP:
            def __init__(self, access_token):
                self.access_token = access_token

            def get_headers(self):
                return {"access-token": self.access_token}

        return DhanHTTP(self.access_token)


CLIENT_ID = "YOUR_CLIENT_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

dhan_context = DhanContext(CLIENT_ID, ACCESS_TOKEN)
dhan = dhanhq(dhan_context)

# 🔥 MARKET SYMBOL (NIFTY)
symbols = {"NSE": ["13"]}

print("Starting MARKET DATA...")

while True:
    try:
        data = dhan.get_market_quote(security_id="13", exchange_segment="NSE_EQ")
        print("TICKS:", data)
    except Exception as e:
        print("ERROR:", e)

    time.sleep(1)

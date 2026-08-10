# ruff: noqa: E501
import time

from dhanhq import dhanhq


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


CLIENT_ID = "1100116730"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg2MjY2OTQ2LCJpYXQiOjE3ODYxODA1NDYsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwMTE2NzMwIn0.iAzU2iXNV08F-FcNtSLYfuQXy-V7EPsPFVhWxcKlFkuxGTuJU1tBKwvErZTeQSrB-FrRn-fXo3pQj0RFcybGwA"

dhan_context = DhanContext(CLIENT_ID, ACCESS_TOKEN)
dhan = dhanhq(dhan_context)

print("Starting MARKET DATA...")

while True:
    try:
        data = dhan.get_market_quote(
            security_id="13",  # NIFTY
            exchange_segment="NSE_EQ",
        )
        print("TICKS:", data)
    except Exception as e:
        print("ERROR:", e)

    time.sleep(1)

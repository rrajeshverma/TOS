import websocket
import json


class LiveMarketFeed:
    def __init__(self, client_id: str, access_token: str):
        self.client_id = client_id
        self.access_token = access_token

    def _on_message(self, ws, message):
        print("TICK:", message)

    def _on_error(self, ws, error):
        print("ERROR:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("CLOSED")

    def _on_open(self, ws):
        print("CONNECTED")

        # ✅ FIXED PAYLOAD (STRING IDS)
        payload = {
            "RequestCode": "15",
            "InstrumentCount": "1",
            "InstrumentList": [{"ExchangeSegment": "NSE_EQ", "SecurityId": "13"}],
        }

        ws.send(json.dumps(payload))

    def run_forever(self):
        url = (
            f"wss://api-feed.dhan.co?"
            f"version=2&token={self.access_token}&clientId={self.client_id}"
        )

        ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

        ws.run_forever()

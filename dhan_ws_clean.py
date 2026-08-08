import asyncio
import websockets
import json

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg2MjY2OTQ2LCJpYXQiOjE3ODYxODA1NDYsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwMTE2NzMwIn0.iAzU2iXNV08F-FcNtSLYfuQXy-V7EPsPFVhWxcKlFkuxGTuJU1tBKwvErZTeQSrB-FrRn-fXo3pQj0RFcybGwA"

WS_URL = "wss://api-feed.dhan.co"


async def connect():
    headers = [("access-token", ACCESS_TOKEN)]

    async with websockets.connect(WS_URL, additional_headers=headers) as ws:
        print("✅ Connected to Dhan WebSocket")

        # Subscribe to NIFTY (securityId = 13)
        subscribe_msg = {
            "RequestCode": 15,
            "InstrumentCount": 1,
            "InstrumentList": [{"ExchangeSegment": "IDX_I", "SecurityId": "13"}],
        }

        await ws.send(json.dumps(subscribe_msg))

        while True:
            data = await ws.recv()
            print("TICK:", data)


asyncio.run(connect())

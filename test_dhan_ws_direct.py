import asyncio
import json
import websockets

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

WS_URL = f"wss://api-feed.dhan.co?token={ACCESS_TOKEN}"


async def connect():
    async with websockets.connect(WS_URL) as ws:
        print("CONNECTED")

        subscribe_msg = {"action": "subscribe", "params": {"symbols": ["NSE:13"]}}

        await ws.send(json.dumps(subscribe_msg))

        while True:
            msg = await ws.recv()
            print("TICKS:", msg)


asyncio.run(connect())

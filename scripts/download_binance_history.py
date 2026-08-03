"""
Download historical Binance candles.

Example:
    python scripts/download_binance_history.py
"""

from __future__ import annotations

import os
from datetime import datetime

import requests

SYMBOL = "BTCUSDT"
INTERVAL = "30m"
LIMIT = 1000

URL = "https://api.binance.com/api/v3/klines"

OUTPUT_DIR = "data/historical/btc"
OUTPUT_FILE = f"{OUTPUT_DIR}/BTCUSDT_30m.csv"


def download():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    response = requests.get(
        URL,
        params={
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT,
        },
        timeout=30,
    )

    response.raise_for_status()

    candles = response.json()

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        f.write("timestamp,open,high,low,close,volume\n")

        for candle in candles:
            timestamp = datetime.utcfromtimestamp(candle[0] / 1000).isoformat()

            f.write(
                f"{timestamp},"
                f"{candle[1]},"
                f"{candle[2]},"
                f"{candle[3]},"
                f"{candle[4]},"
                f"{candle[5]}\n"
            )

    print(f"Downloaded {len(candles)} candles.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    download()

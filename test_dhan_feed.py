from dhanhq import DhanContext, MarketFeed

from config.system import DHAN_ACCESS_TOKEN, DHAN_CLIENT_ID

print("Starting feed...")

context = DhanContext(
    DHAN_CLIENT_ID,
    DHAN_ACCESS_TOKEN,
)


def on_connect(feed):
    print("✅ Connected to Dhan Feed")


def on_close(feed):
    print("❌ Connection closed")


def on_error(feed, error):
    print("❌ Error:", error)


def on_ticks(feed, data):
    print("📈 TICK:", data)


instruments = [
    (
        MarketFeed.IDX,
        "13",
        MarketFeed.Quote,  # ✅ IMPORTANT
    ),
]

feed = MarketFeed(
    dhan_context=context,
    instruments=instruments,
    version="v2",
    on_connect=on_connect,
    on_close=on_close,
    on_error=on_error,
    on_ticks=on_ticks,
)

feed.run_forever()

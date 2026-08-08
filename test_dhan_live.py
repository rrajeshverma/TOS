from brokers.dhan.live_market_feed import LiveMarketFeed
from config.system import DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN

feed = LiveMarketFeed(DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN)
feed.run_forever()

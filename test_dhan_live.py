from brokers.dhan.live_market_feed import LiveMarketFeed
from config.system import DHAN_ACCESS_TOKEN, DHAN_CLIENT_ID

feed = LiveMarketFeed(DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN)
feed.run_forever()

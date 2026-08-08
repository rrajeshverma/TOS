from dhanhq import dhanhq
from dhanhq.marketfeed import MarketFeed

CLIENT_ID = "1100116730"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg2MjY2OTQ2LCJpYXQiOjE3ODYxODA1NDYsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwMTE2NzMwIn0.iAzU2iXNV08F-FcNtSLYfuQXy-V7EPsPFVhWxcKlFkuxGTuJU1tBKwvErZTeQSrB-FrRn-fXo3pQj0RFcybGwA"


dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

instruments = [(MarketFeed.IDX, "13", MarketFeed.QUOTE)]

feed = MarketFeed(dhan, instruments)


def on_message(msg):
    print("TICK:", msg)


feed.on_message = on_message

feed.run_forever()

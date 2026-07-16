from brokers.clients.dhan_client import DhanClient


client = DhanClient()

print(client.get_fund_limits())
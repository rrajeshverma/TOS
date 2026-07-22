from config.system import (
    BROKER,
    DHAN_ACCESS_TOKEN,
    DHAN_CLIENT_ID,
)

print("Broker     :", BROKER)
print("Client ID  :", DHAN_CLIENT_ID)
print("Token Found:", DHAN_ACCESS_TOKEN is not None)

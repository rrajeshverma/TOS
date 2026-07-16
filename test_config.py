from config.system import (
    DHAN_CLIENT_ID,
    DHAN_ACCESS_TOKEN,
    BROKER,
)

print("Broker     :", BROKER)
print("Client ID  :", DHAN_CLIENT_ID)
print("Token Found:", DHAN_ACCESS_TOKEN is not None)
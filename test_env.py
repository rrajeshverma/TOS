from config.system import DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN

print("Client ID:", DHAN_CLIENT_ID)

if DHAN_ACCESS_TOKEN:
    print("Token Length:", len(DHAN_ACCESS_TOKEN))
    print("Token Prefix:", DHAN_ACCESS_TOKEN[:10])
else:
    print("Token missing")

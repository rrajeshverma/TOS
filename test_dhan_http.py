import requests
import time

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg2MjY2OTQ2LCJpYXQiOjE3ODYxODA1NDYsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwMTE2NzMwIn0.iAzU2iXNV08F-FcNtSLYfuQXy-V7EPsPFVhWxcKlFkuxGTuJU1tBKwvErZTeQSrB-FrRn-fXo3pQj0RFcybGwA"


URL = "https://api.dhan.co/v2/market/quote"  # ✅ CORRECT ENDPOINT

headers = {"access-token": ACCESS_TOKEN, "Content-Type": "application/json"}

payload = {
    "securityId": ["13"],  # Example: NIFTY = 13 (Dhan format)
    "exchangeSegment": "IDX_I",
}

print("Starting MARKET DATA DEBUG...")

while True:
    try:
        response = requests.post(URL, headers=headers, json=payload)

        print("STATUS:", response.status_code)
        print("RAW:", response.text)  # 👈 IMPORTANT

        data = response.json()
        print("PARSED:", data)

    except Exception as e:
        print("ERROR:", e)

    time.sleep(2)

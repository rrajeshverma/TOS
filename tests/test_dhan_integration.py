import os

from dotenv import load_dotenv

from brokers.clients.dhan_client import DhanClient

load_dotenv()


def main():
    client = DhanClient(
        client_id=os.getenv("DHAN_CLIENT_ID"),
        access_token=os.getenv("DHAN_ACCESS_TOKEN"),
    )

    print(client.get_fund_limits())


if __name__ == "__main__":
    main()

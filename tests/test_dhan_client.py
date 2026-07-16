from brokers.clients.dhan_client import DhanClient


def test_client_created():
    client = DhanClient()

    assert client is not None
    assert client.sdk is not None
from brokers.dhan_broker import DhanBroker
from brokers.paper_broker import PaperBroker


class BrokerFactory:

    @staticmethod
    def create(name: str, client=None):
        name = name.lower()

        if name == "paper":
            return PaperBroker()

        if name == "dhan":
            if client is None:
                raise ValueError("client is required for DhanBroker")

            return DhanBroker(client)

        raise ValueError(f"Unsupported broker: {name}")
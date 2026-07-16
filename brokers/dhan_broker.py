from decimal import Decimal

from brokers.base_broker import BaseBroker
from brokers.models import (
    Funds,
    Position,
)

class DhanBroker(BaseBroker):
    """Broker implementation backed by Dhan."""

    def __init__(self, client):
        self.client = client

    def get_funds(self) -> Funds:

        response = self.client.get_fund_limits()

        data = response["data"]

        available_cash = Decimal(str(data["availabelBalance"]))
        utilised_margin = Decimal(str(data["utilizedAmount"]))

        return Funds(
            available_cash=available_cash,
            utilised_margin=utilised_margin,
            available_margin=available_cash - utilised_margin,
        )

    # Remaining methods
    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def is_connected(self):
        raise NotImplementedError

    def place_order(self, order):
        raise NotImplementedError

    def modify_order(self, order_id, **kwargs):
        raise NotImplementedError

    def cancel_order(self, order_id):
        raise NotImplementedError

    def get_order(self, order_id):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError

    from brokers.models import Position
    def get_positions(self):

        response = self.client.get_positions()

        positions = []

        for item in response["data"]:

            positions.append(
                Position(
                    symbol=item["tradingSymbol"],
                    quantity=item["netQty"],
                    average_price=Decimal(str(item["costPrice"])),
                    last_price=Decimal(str(item["lastTradedPrice"])),
                    pnl=Decimal("0"),
                )
            )

        return positions

    def get_holdings(self):
        raise NotImplementedError
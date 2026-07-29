from dataclasses import replace
from decimal import Decimal

from brokers.base_broker import BaseBroker
from brokers.dhan_mapper import DhanMapper
from brokers.models import (
    Funds,
    Holding,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Position,
    ProductType,
)


class DhanBroker(BaseBroker):
    def __init__(self, client, instrument_mapper):
        self.client = client
        self.instrument_mapper = instrument_mapper

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
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def is_connected(self):
        return bool(
            getattr(
                self.client,
                "connected",
                False,
            )
        )

    def place_order(self, order):
        if not self.is_connected():
            raise RuntimeError("Dhan broker is not connected.")
        instrument = self.instrument_mapper.get(order.symbol)

        if instrument is None:
            raise ValueError(f"Instrument not found: {order.symbol}")

        response = self.client.place_order(
            security_id=instrument.security_id,
            exchange_segment=instrument.exchange_segment,
            transaction_type=DhanMapper.transaction_type(order.side),
            quantity=order.quantity,
            order_type=DhanMapper.order_type(order.order_type),
            product_type=DhanMapper.product_type(order.product),
            price=float(order.price or 0),
            trigger_price=float(order.trigger_price or 0),
        )

        order_id = response["data"]["orderId"]

        return replace(
            order,
            broker_order_id=order_id,
            status=OrderStatus.PENDING,
        )

    def modify_order(self, order_id, **kwargs):
        return self.client.modify_order(
            order_id,
            kwargs,
        )

    def cancel_order(self, order_id: str):
        """Cancel an existing order."""
        return self.client.cancel_order(order_id)

    def get_order(self, order_id):
        item = self.client.get_order(order_id)

        return Order(
            symbol=item["tradingSymbol"],
            side=OrderSide(item["transactionType"]),
            quantity=item["quantity"],
            order_type=OrderType(item["orderType"]),
            product=ProductType(item["productType"]),
            broker_order_id=item["orderId"],
            status=OrderStatus(item["orderStatus"]),
        )

    def get_orders(self):
        response = self.client.get_order_list()

        orders = []

        for item in response["data"]:
            orders.append(
                Order(
                    symbol=item["tradingSymbol"],
                    side=OrderSide(item["transactionType"]),
                    quantity=item["quantity"],
                    order_type=OrderType(item["orderType"]),
                    product=ProductType(item["productType"]),
                    broker_order_id=item["orderId"],
                    status=OrderStatus(item["orderStatus"]),
                )
            )

        return orders

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
        response = self.client.get_holdings()

        holdings = []

        for item in response["data"]:
            holdings.append(
                Holding(
                    symbol=item["tradingSymbol"],
                    quantity=item["totalQty"],
                    average_price=Decimal(str(item["avgCostPrice"])),
                )
            )

        return holdings

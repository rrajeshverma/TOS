from decimal import Decimal

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


class DhanMapper:
    @staticmethod
    def transaction_type(side: OrderSide) -> str:
        return side.value

    @staticmethod
    def order_type(order_type: OrderType) -> str:
        return order_type.value

    @staticmethod
    def product_type(product: ProductType) -> str:
        return product.value

    @staticmethod
    def to_funds(data: dict) -> Funds:
        available_cash = Decimal(str(data["availabelBalance"]))
        utilised_margin = Decimal(str(data["utilizedAmount"]))

        return Funds(
            available_cash=available_cash,
            utilised_margin=utilised_margin,
            available_margin=available_cash - utilised_margin,
        )

    @staticmethod
    def to_order(item: dict) -> Order:
        return Order(
            symbol=item["tradingSymbol"],
            side=OrderSide(item["transactionType"]),
            quantity=item["quantity"],
            order_type=OrderType(item["orderType"]),
            product=ProductType(item["productType"]),
            broker_order_id=item["orderId"],
            status=OrderStatus(item["orderStatus"]),
        )

    @staticmethod
    def to_position(item: dict) -> Position:
        return Position(
            symbol=item["tradingSymbol"],
            quantity=item["netQty"],
            average_price=Decimal(str(item["costPrice"])),
            last_price=Decimal(str(item["lastTradedPrice"])),
            pnl=Decimal(0),
        )

    @staticmethod
    def to_holding(item: dict) -> Holding:
        return Holding(
            symbol=item["tradingSymbol"],
            quantity=item["totalQty"],
            average_price=Decimal(str(item["avgCostPrice"])),
        )

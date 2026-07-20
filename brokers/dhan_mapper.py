from brokers.models import OrderSide, OrderType, ProductType


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

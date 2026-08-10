"""
Broker domain models.

These models provide a broker-agnostic representation of
orders, positions, holdings, and funds.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"
    SL_MARKET = "SL_MARKET"


class ProductType(Enum):
    INTRADAY = "INTRADAY"
    DELIVERY = "DELIVERY"


class OrderStatus(Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    COMPLETE = "COMPLETE"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass(slots=True)
class Order:
    symbol: str
    side: OrderSide
    quantity: int
    order_type: OrderType
    product: ProductType

    price: Decimal | None = None
    trigger_price: Decimal | None = None

    broker_order_id: str | None = None
    status: OrderStatus = OrderStatus.PENDING


@dataclass(slots=True)
class Position:
    symbol: str
    quantity: int
    average_price: Decimal
    last_price: Decimal
    pnl: Decimal


@dataclass(slots=True)
class Holding:
    symbol: str
    quantity: int
    average_price: Decimal


@dataclass(slots=True)
class Funds:
    available_cash: Decimal
    utilised_margin: Decimal
    available_margin: Decimal

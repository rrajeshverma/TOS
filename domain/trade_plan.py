from dataclasses import dataclass
from decimal import Decimal

from domain.decision import Decision


@dataclass(frozen=True, slots=True)
class TradePlan:
    decision: Decision
    entry_price: Decimal
    stop_loss: Decimal
    target_price: Decimal
    lots: int
    quantity: int
    risk_amount: Decimal
    reward_amount: Decimal

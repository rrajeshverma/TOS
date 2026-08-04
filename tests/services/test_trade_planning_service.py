from decimal import Decimal

from services.trade_planning_service import (
    TradePlanningService,
)
from tests.helpers.domain_factory import make_decision


def test_create_trade_plan():
    service = TradePlanningService()

    plan = service.create_trade_plan(
        decision=make_decision(),
        entry_price=Decimal("250"),
        stop_loss=Decimal("240"),
        target_price=Decimal("270"),
        risk_per_trade=Decimal("2500"),
        lot_size=65,
    )

    assert plan.entry_price == Decimal("250")
    assert plan.stop_loss == Decimal("240")
    assert plan.target_price == Decimal("270")
    assert plan.position_size.lots > 0
    assert plan.position_size.quantity > 0

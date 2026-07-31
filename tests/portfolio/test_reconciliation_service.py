from dataclasses import dataclass

from portfolio.reconciliation_service import ReconciliationService


@dataclass
class Position:
    symbol: str
    quantity: int


def test_matching_positions():
    service = ReconciliationService()

    broker = [Position("NIFTY", 1)]
    local = [Position("NIFTY", 1)]

    assert service.reconcile(broker, local) == []


def test_quantity_mismatch():
    service = ReconciliationService()

    broker = [Position("NIFTY", 2)]
    local = [Position("NIFTY", 1)]

    result = service.reconcile(broker, local)

    assert len(result) == 1
    assert result[0]["symbol"] == "NIFTY"


def test_missing_local_position():
    service = ReconciliationService()

    broker = [Position("BANKNIFTY", 1)]
    local = []

    result = service.reconcile(broker, local)

    assert result[0]["broker"] == 1
    assert result[0]["local"] == 0

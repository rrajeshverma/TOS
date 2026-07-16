from decimal import Decimal

from brokers.dhan_broker import DhanBroker
from brokers.models import Funds, Position
from brokers.models import Holding

class DummyClient:

    def get_fund_limits(self):
        return {
            "status": "success",
            "data": {
                "availabelBalance": 100000.00,
                "utilizedAmount": 5000.00,
            },
        }


class DummyPositionClient:

    def get_positions(self):
        return {
            "status": "success",
            "data": [
                {
                    "securityId": "13",
                    "tradingSymbol": "NIFTY",
                    "netQty": 65,
                    "costPrice": 245.50,
                    "lastTradedPrice": 250.25,
                }
            ],
        }


def test_get_funds():
    broker = DhanBroker(DummyClient())

    funds = broker.get_funds()

    assert isinstance(funds, Funds)
    assert funds.available_cash == Decimal("100000.00")
    assert funds.utilised_margin == Decimal("5000.00")
    assert funds.available_margin == Decimal("95000.00")


def test_get_positions():
    broker = DhanBroker(DummyPositionClient())

    positions = broker.get_positions()

    assert len(positions) == 1

    assert isinstance(positions[0], Position)

    assert positions[0].symbol == "NIFTY"
    assert positions[0].quantity == 65
    assert positions[0].average_price == Decimal("245.50")
    assert positions[0].last_price == Decimal("250.25")
    assert positions[0].pnl == Decimal("0")

class DummyHoldingClient:

    def get_holdings(self):
        return {
            "status": "success",
            "data": [
                {
                    "tradingSymbol": "RELIANCE",
                    "totalQty": 10,
                    "avgCostPrice": 2500.50,
                }
            ],
        }


def test_get_holdings():

    broker = DhanBroker(DummyHoldingClient())

    holdings = broker.get_holdings()

    assert len(holdings) == 1

    assert isinstance(holdings[0], Holding)

    assert holdings[0].symbol == "RELIANCE"
    assert holdings[0].quantity == 10
    assert holdings[0].average_price == Decimal("2500.50")
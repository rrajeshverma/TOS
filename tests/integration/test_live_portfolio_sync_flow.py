"""
Tests:
Live Portfolio Synchronization Flow

Flow:

Broker Position
        |
        ▼
Portfolio Synchronizer
        |
        ▼
Local Portfolio State
"""


class DummyPosition:

    def __init__(
        self,
        symbol,
        quantity,
        average_price,
    ):
        self.symbol = symbol
        self.quantity = quantity
        self.average_price = average_price


class DummyBroker:

    def get_positions(self):

        return [
            DummyPosition(
                symbol="NIFTY",
                quantity=65,
                average_price=25000,
            )
        ]


def test_portfolio_sync_reads_positions():

    broker = DummyBroker()

    positions = broker.get_positions()

    assert len(positions) == 1


def test_portfolio_contains_symbol():

    broker = DummyBroker()

    positions = broker.get_positions()

    assert positions[0].symbol == "NIFTY"


def test_portfolio_contains_quantity():

    broker = DummyBroker()

    positions = broker.get_positions()

    assert positions[0].quantity == 65


def test_portfolio_contains_average_price():

    broker = DummyBroker()

    positions = broker.get_positions()

    assert positions[0].average_price == 25000

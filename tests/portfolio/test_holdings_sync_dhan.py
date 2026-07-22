from unittest.mock import Mock

from portfolio.holdings_sync import HoldingsSync


def test_sync_holdings_from_broker():
    broker = Mock()

    broker.get_holdings.return_value = [
        {
            "securityId": "500325",
            "quantity": 10,
        },
        {
            "securityId": "532540",
            "quantity": 20,
        },
    ]

    sync = HoldingsSync(broker)

    holdings = sync.sync()

    broker.get_holdings.assert_called_once_with()

    assert len(holdings) == 2
    assert holdings[0]["securityId"] == "500325"

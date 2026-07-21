from unittest.mock import Mock

from portfolio.account_sync import AccountSync
from portfolio.holdings_sync import HoldingsSync
from portfolio.position_sync import PositionSync
from portfolio.sync import BrokerSyncService


def test_complete_broker_sync():
    broker = Mock()

    broker.get_positions.return_value = [
        {"securityId": "NIFTY", "quantity": 50},
    ]

    broker.get_holdings.return_value = [
        {"securityId": "INFY", "quantity": 10},
    ]

    broker.get_funds.return_value = {
        "availableBalance": 100000,
    }

    service = BrokerSyncService(
        position_sync=PositionSync(broker),
        holdings_sync=HoldingsSync(broker),
        account_sync=AccountSync(broker),
    )

    result = service.sync_all()

    assert result["positions"][0]["securityId"] == "NIFTY"
    assert result["holdings"][0]["securityId"] == "INFY"
    assert result["account"]["availableBalance"] == 100000
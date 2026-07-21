from unittest.mock import Mock

from execution.order_service import OrderService
from portfolio.account_sync import AccountSync
from portfolio.holdings_sync import HoldingsSync
from portfolio.position_sync import PositionSync
from portfolio.sync import BrokerSyncService


def test_production_components_can_be_created():
    broker = Mock()

    order_service = OrderService(broker=broker)

    sync_service = BrokerSyncService(
        position_sync=PositionSync(broker),
        holdings_sync=HoldingsSync(broker),
        account_sync=AccountSync(broker),
    )

    assert order_service is not None
    assert sync_service is not None
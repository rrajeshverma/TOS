from unittest.mock import Mock

from portfolio.sync import BrokerSyncService


def test_sync_all_calls_every_sync():
    position_sync = Mock()
    holdings_sync = Mock()
    account_sync = Mock()

    position_sync.sync.return_value = ["positions"]
    holdings_sync.sync.return_value = ["holdings"]
    account_sync.sync.return_value = {"funds": 100000}

    service = BrokerSyncService(
        position_sync=position_sync,
        holdings_sync=holdings_sync,
        account_sync=account_sync,
    )

    result = service.sync_all()

    position_sync.sync.assert_called_once_with()
    holdings_sync.sync.assert_called_once_with()
    account_sync.sync.assert_called_once_with()

    assert result["positions"] == ["positions"]
    assert result["holdings"] == ["holdings"]
    assert result["account"] == {"funds": 100000}
    assert result["errors"] == {}
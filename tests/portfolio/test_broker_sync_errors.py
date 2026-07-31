from unittest.mock import Mock

from portfolio.sync import BrokerSyncService


def test_sync_all_returns_error_for_failed_position_sync():
    position_sync = Mock()
    holdings_sync = Mock()
    account_sync = Mock()

    position_sync.sync.side_effect = RuntimeError("Broker unavailable")
    holdings_sync.sync.return_value = ["holdings"]
    account_sync.sync.return_value = {"funds": 100000}

    service = BrokerSyncService(
        position_sync=position_sync,
        holdings_sync=holdings_sync,
        account_sync=account_sync,
    )

    result = service.sync_all()

    assert result["positions"] is None
    assert result["holdings"] == ["holdings"]
    assert result["account"] == {"funds": 100000}

    assert result["errors"]["positions"] == "Broker unavailable"

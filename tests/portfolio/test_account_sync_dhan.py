from unittest.mock import Mock

from portfolio.account_sync import AccountSync


def test_sync_account_from_broker():
    broker = Mock()

    broker.get_funds.return_value = {
        "availableBalance": 250000.00,
        "utilizedMargin": 50000.00,
    }

    sync = AccountSync(broker)

    funds = sync.sync()

    broker.get_funds.assert_called_once_with()

    assert funds["availableBalance"] == 250000.00
    assert funds["utilizedMargin"] == 50000.00

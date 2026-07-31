from portfolio.sync import BrokerSyncService


def test_sync_all_returns_success_status():
    class Sync:
        def sync(self):
            return "OK"

    service = BrokerSyncService(
        Sync(),
        Sync(),
        Sync(),
    )

    result = service.sync_all()

    assert result["success"] is True


def test_sync_all_returns_failure_status():
    class Bad:
        def sync(self):
            raise Exception("broker failed")

    service = BrokerSyncService(
        Bad(),
        Bad(),
        Bad(),
    )

    result = service.sync_all()

    assert result["success"] is False

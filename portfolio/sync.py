from dataclasses import dataclass


@dataclass
class BrokerSyncService:
    position_sync: object
    holdings_sync: object
    account_sync: object

    def sync_all(self):
        results = {
            "positions": None,
            "holdings": None,
            "account": None,
            "errors": {},
        }

        syncers = {
            "positions": self.position_sync,
            "holdings": self.holdings_sync,
            "account": self.account_sync,
        }

        for name, syncer in syncers.items():
            try:
                results[name] = syncer.sync()
            except Exception as exc:
                results["errors"][name] = str(exc)

        return results
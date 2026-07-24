from runtime.recovery_manager import RecoveryManager


class FakeBroker:
    def get_orders(self):
        return []

    def get_positions(self):
        return []

    def get_holdings(self):
        return []

    def get_funds(self):
        return {}


def test_recovery():
    manager = RecoveryManager(FakeBroker())

    state = manager.recover()

    assert state["orders"] == []
    assert state["positions"] == []
    assert state["holdings"] == []
    assert state["funds"] == {}

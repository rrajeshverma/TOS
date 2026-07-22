from services.order_execution_adapter import OrderExecutionAdapter


class FakeBroker:

    def __init__(self, connected=True):
        self.connected = connected
        self.called = False

    def is_connected(self):
        return self.connected

    def place_order(self, order):
        self.called = True
        return {
            "status": "SUCCESS",
            "order": order,
        }


def test_adapter_rejects_disconnected_broker():

    broker = FakeBroker(False)

    adapter = OrderExecutionAdapter(
        broker=broker
    )

    try:
        adapter.execute(
            {"symbol": "NIFTY"}
        )

        assert False

    except RuntimeError:
        assert True


def test_adapter_executes_connected_broker():

    broker = FakeBroker(True)

    adapter = OrderExecutionAdapter(
        broker=broker
    )

    result = adapter.execute(
        {"symbol": "NIFTY"}
    )

    assert result["status"] == "SUCCESS"
    assert broker.called is True
"""
=========================================================
Trading Operating System (TOS)
Module      : Order Execution Adapter Tests
Version     : 1.1.0
=========================================================
"""

import pytest

from unittest.mock import Mock

from services.order_execution_adapter import OrderExecutionAdapter


def test_to_execution_order_none_raises_value_error():
    adapter = OrderExecutionAdapter()

    with pytest.raises(ValueError, match="Order cannot be None."):
        adapter.to_execution_order(None)


def test_execute_without_broker_raises_runtime_error():
    adapter = OrderExecutionAdapter()

    with pytest.raises(
        RuntimeError,
        match="Execution service is not configured.",
    ):
        adapter.execute({"symbol": "NIFTY"})


class DummyIdempotency:
    def __init__(self):
        self.store = {}

    def is_duplicate(self, key):
        return key in self.store

    def get(self, key):
        return self.store[key]

    def record(self, key, value):
        self.store[key] = value


class DummyOrderService:
    def place_order(self, order):
        return {"id": 101, "status": "placed"}


class DummyBroker:
    def __init__(self, connected=True):
        self.connected = connected

    def is_connected(self):
        return self.connected

    def place_order(self, order):
        return {"broker": "DHAN", "status": "placed"}


def test_execute_duplicate_returns_cached_result():
    idem = DummyIdempotency()

    order = {"symbol": "NIFTY"}

    key = str(sorted(order.items()))

    idem.record(key, {"cached": True})

    adapter = OrderExecutionAdapter(
        idempotency=idem,
    )

    assert adapter.execute(order) == {"cached": True}


def test_execute_uses_order_service():
    adapter = OrderExecutionAdapter(
        order_service=DummyOrderService(),
        idempotency=DummyIdempotency(),
    )

    result = adapter.execute({"symbol": "NIFTY"})

    assert result["status"] == "placed"


def test_execute_broker_not_connected():
    adapter = OrderExecutionAdapter(
        broker=DummyBroker(False),
        idempotency=DummyIdempotency(),
    )

    with pytest.raises(
        RuntimeError,
        match="Broker is not connected.",
    ):
        adapter.execute({"symbol": "NIFTY"})


def test_execute_broker_success():
    adapter = OrderExecutionAdapter(
        broker=DummyBroker(True),
        idempotency=DummyIdempotency(),
    )

    result = adapter.execute({"symbol": "NIFTY"})

    assert result["broker"] == "DHAN"


def test_execute_records_idempotency():
    idem = DummyIdempotency()

    adapter = OrderExecutionAdapter(
        broker=DummyBroker(True),
        idempotency=idem,
    )

    order = {"symbol": "NIFTY"}

    adapter.execute(order)

    key = str(sorted(order.items()))

    assert idem.is_duplicate(key)


def test_execute_duplicate_does_not_call_order_service():
    idem = DummyIdempotency()

    order = {"symbol": "NIFTY"}
    key = str(sorted(order.items()))

    idem.record(key, {"cached": True})

    service = Mock()

    adapter = OrderExecutionAdapter(
        order_service=service,
        idempotency=idem,
    )

    result = adapter.execute(order)

    assert result == {"cached": True}
    service.place_order.assert_not_called()


def test_execute_duplicate_does_not_call_broker():
    idem = DummyIdempotency()

    order = {"symbol": "NIFTY"}
    key = str(sorted(order.items()))

    idem.record(key, {"cached": True})

    broker = Mock()

    adapter = OrderExecutionAdapter(
        broker=broker,
        idempotency=idem,
    )

    result = adapter.execute(order)

    assert result == {"cached": True}
    broker.place_order.assert_not_called()


def test_execute_with_broker_without_is_connected():
    class Broker:
        def place_order(self, order):
            return {"status": "placed"}

    adapter = OrderExecutionAdapter(
        broker=Broker(),
        idempotency=DummyIdempotency(),
    )

    result = adapter.execute({"symbol": "NIFTY"})

    assert result["status"] == "placed"


def test_order_service_result_cached():
    idem = DummyIdempotency()

    adapter = OrderExecutionAdapter(
        order_service=DummyOrderService(),
        idempotency=idem,
    )

    order = {"symbol": "NIFTY"}

    result = adapter.execute(order)

    key = str(sorted(order.items()))

    assert idem.get(key) == result


def test_broker_result_cached():
    idem = DummyIdempotency()

    adapter = OrderExecutionAdapter(
        broker=DummyBroker(True),
        idempotency=idem,
    )

    order = {"symbol": "NIFTY"}

    result = adapter.execute(order)

    key = str(sorted(order.items()))

    assert idem.get(key) == result

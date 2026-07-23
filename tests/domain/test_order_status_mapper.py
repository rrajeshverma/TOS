import pytest

from brokers.models import OrderStatus as BrokerOrderStatus
from domain.order_status_mapper import OrderStatusMapper
from execution.order_service import OrderStatus as ExecutionOrderStatus
from shared.enums import OrderStatus as DomainOrderStatus


# ---------------------------------------------------------------------
# Broker -> Execution
# ---------------------------------------------------------------------


def test_broker_pending_maps_to_execution_pending():
    assert (
        OrderStatusMapper.broker_to_execution(BrokerOrderStatus.PENDING)
        == ExecutionOrderStatus.PENDING
    )


def test_broker_open_maps_to_execution_submitted():
    assert (
        OrderStatusMapper.broker_to_execution(BrokerOrderStatus.OPEN)
        == ExecutionOrderStatus.SUBMITTED
    )


def test_broker_complete_maps_to_execution_filled():
    assert (
        OrderStatusMapper.broker_to_execution(BrokerOrderStatus.COMPLETE)
        == ExecutionOrderStatus.FILLED
    )


def test_broker_cancelled_maps_to_execution_cancelled():
    assert (
        OrderStatusMapper.broker_to_execution(BrokerOrderStatus.CANCELLED)
        == ExecutionOrderStatus.CANCELLED
    )


def test_broker_rejected_maps_to_execution_cancelled():
    assert (
        OrderStatusMapper.broker_to_execution(BrokerOrderStatus.REJECTED)
        == ExecutionOrderStatus.CANCELLED
    )


def test_unknown_broker_status_raises_value_error():
    with pytest.raises(
        ValueError,
        match="Unsupported broker order status",
    ):
        OrderStatusMapper.broker_to_execution("INVALID")


# ---------------------------------------------------------------------
# Execution -> Domain
# ---------------------------------------------------------------------


def test_execution_new_maps_to_domain_created():
    assert (
        OrderStatusMapper.execution_to_domain(ExecutionOrderStatus.NEW)
        == DomainOrderStatus.CREATED
    )


def test_execution_pending_maps_to_domain_pending():
    assert (
        OrderStatusMapper.execution_to_domain(ExecutionOrderStatus.PENDING)
        == DomainOrderStatus.PENDING
    )


def test_execution_submitted_maps_to_domain_pending():
    assert (
        OrderStatusMapper.execution_to_domain(ExecutionOrderStatus.SUBMITTED)
        == DomainOrderStatus.PENDING
    )


def test_execution_partially_filled_maps_to_domain_pending():
    assert (
        OrderStatusMapper.execution_to_domain(ExecutionOrderStatus.PARTIALLY_FILLED)
        == DomainOrderStatus.PENDING
    )


def test_execution_filled_maps_to_domain_executed():
    assert (
        OrderStatusMapper.execution_to_domain(ExecutionOrderStatus.FILLED)
        == DomainOrderStatus.EXECUTED
    )


def test_execution_cancelled_maps_to_domain_cancelled():
    assert (
        OrderStatusMapper.execution_to_domain(ExecutionOrderStatus.CANCELLED)
        == DomainOrderStatus.CANCELLED
    )


def test_unknown_execution_status_raises_value_error():
    with pytest.raises(
        ValueError,
        match="Unsupported execution order status",
    ):
        OrderStatusMapper.execution_to_domain("INVALID")


# ---------------------------------------------------------------------
# Consistency
# ---------------------------------------------------------------------


def test_every_broker_mapping_returns_execution_status():
    for status in OrderStatusMapper.BROKER_TO_EXECUTION:
        result = OrderStatusMapper.broker_to_execution(status)

        assert isinstance(
            result,
            ExecutionOrderStatus,
        )


def test_every_execution_mapping_returns_domain_status():
    for status in OrderStatusMapper.EXECUTION_TO_DOMAIN:
        result = OrderStatusMapper.execution_to_domain(status)

        assert isinstance(
            result,
            DomainOrderStatus,
        )


def test_broker_mapping_contains_expected_entries():
    assert len(OrderStatusMapper.BROKER_TO_EXECUTION) == 5


def test_execution_mapping_contains_expected_entries():
    assert len(OrderStatusMapper.EXECUTION_TO_DOMAIN) == 6

import pytest

from domain.order_status_mapper import OrderStatusMapper
from shared.enums import OrderStatus as DomainOrderStatus
from execution.order_service import OrderStatus as ExecutionOrderStatus
from brokers.models import OrderStatus as BrokerOrderStatus


@pytest.mark.parametrize(
    "broker_status,expected",
    [
        (
            BrokerOrderStatus.PENDING,
            ExecutionOrderStatus.PENDING,
        ),
        (
            BrokerOrderStatus.OPEN,
            ExecutionOrderStatus.SUBMITTED,
        ),
        (
            BrokerOrderStatus.COMPLETE,
            ExecutionOrderStatus.FILLED,
        ),
        (
            BrokerOrderStatus.CANCELLED,
            ExecutionOrderStatus.CANCELLED,
        ),
        (
            BrokerOrderStatus.REJECTED,
            ExecutionOrderStatus.CANCELLED,
        ),
    ],
)
def test_broker_to_execution(
    broker_status,
    expected,
):
    assert (
        OrderStatusMapper.broker_to_execution(broker_status)
        == expected
    )


@pytest.mark.parametrize(
    "execution_status,expected",
    [
        (
            ExecutionOrderStatus.NEW,
            DomainOrderStatus.CREATED,
        ),
        (
            ExecutionOrderStatus.PENDING,
            DomainOrderStatus.PENDING,
        ),
        (
            ExecutionOrderStatus.FILLED,
            DomainOrderStatus.EXECUTED,
        ),
        (
            ExecutionOrderStatus.CANCELLED,
            DomainOrderStatus.CANCELLED,
        ),
    ],
)
def test_execution_to_domain(
    execution_status,
    expected,
):
    assert (
        OrderStatusMapper.execution_to_domain(execution_status)
        == expected
    )
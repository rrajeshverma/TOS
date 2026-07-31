"""
=========================================================
Trading Operating System (TOS)
Module      : Order Status Mapper
Version     : 1.0.0
Description : Maps order statuses between system layers.
=========================================================
"""

from brokers.models import OrderStatus as BrokerOrderStatus
from execution.order_service import OrderStatus as ExecutionOrderStatus
from shared.enums import OrderStatus as DomainOrderStatus


class OrderStatusMapper:
    """
    Converts order status between:

    Broker Layer
        ↓
    Execution Layer
        ↓
    Domain Layer
    """

    BROKER_TO_EXECUTION = {
        BrokerOrderStatus.PENDING: ExecutionOrderStatus.PENDING,
        BrokerOrderStatus.OPEN: ExecutionOrderStatus.SUBMITTED,
        BrokerOrderStatus.COMPLETE: ExecutionOrderStatus.FILLED,
        BrokerOrderStatus.CANCELLED: ExecutionOrderStatus.CANCELLED,
        BrokerOrderStatus.REJECTED: ExecutionOrderStatus.CANCELLED,
    }

    EXECUTION_TO_DOMAIN = {
        ExecutionOrderStatus.NEW: DomainOrderStatus.CREATED,
        ExecutionOrderStatus.PENDING: DomainOrderStatus.PENDING,
        ExecutionOrderStatus.SUBMITTED: DomainOrderStatus.PENDING,
        ExecutionOrderStatus.PARTIALLY_FILLED: DomainOrderStatus.PENDING,
        ExecutionOrderStatus.FILLED: DomainOrderStatus.EXECUTED,
        ExecutionOrderStatus.CANCELLED: DomainOrderStatus.CANCELLED,
    }

    @classmethod
    def broker_to_execution(
        cls,
        status: BrokerOrderStatus,
    ) -> ExecutionOrderStatus:
        """
        Convert broker status to execution status.
        """

        try:
            return cls.BROKER_TO_EXECUTION[status]
        except KeyError as exc:
            raise ValueError(f"Unsupported broker order status: {status}") from exc

    @classmethod
    def execution_to_domain(
        cls,
        status: ExecutionOrderStatus,
    ) -> DomainOrderStatus:
        """
        Convert execution status to domain status.
        """

        try:
            return cls.EXECUTION_TO_DOMAIN[status]
        except KeyError as exc:
            raise ValueError(f"Unsupported execution order status: {status}") from exc

"""
Execution Repository

Persistence abstraction for execution tracking.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ExecutionRepository(ABC):
    """
    Repository interface for execution state.
    """

    @abstractmethod
    def save(
        self,
        order_id: str,
        data,
    ) -> None:
        """
        Save execution state.
        """

    @abstractmethod
    def load(
        self,
        order_id: str,
    ):
        """
        Load execution state.
        """

    @abstractmethod
    def exists(
        self,
        order_id: str,
    ) -> bool:
        """
        Return True if order exists.
        """

    @abstractmethod
    def delete(
        self,
        order_id: str,
    ) -> None:
        """
        Delete execution state.
        """

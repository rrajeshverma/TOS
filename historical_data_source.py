"""
Historical data source interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.market import Market


class HistoricalDataSource(ABC):
    """
    Base interface for historical market data sources.
    """

    @abstractmethod
    def load(self) -> list[Market]:
        """
        Load historical market data.

        Returns:
            List of Market objects ordered by timestamp.
        """
        raise NotImplementedError

"""
Historical data source interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

from domain.market import Market


class HistoricalDataSource(ABC):
    """
    Base interface for all historical data sources.
    """

    @abstractmethod
    def load(
        self,
        source: Path | str,
        **kwargs,
    ) -> Iterator[Market]:
        """
        Load historical market data.
        """
        raise NotImplementedError

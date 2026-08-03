from abc import ABC, abstractmethod
from collections.abc import Iterable

from domain.instrument import Instrument


class BaseInstrumentProvider(ABC):
    """Base instrument provider."""

    @abstractmethod
    def load(self) -> Iterable[Instrument]:
        """Load instruments."""

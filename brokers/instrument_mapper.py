from domain.instrument import Instrument
from storage.instrument_repository import InstrumentRepository


class InstrumentMapper:
    def __init__(self, repository: InstrumentRepository):
        self._repository = repository

    def get(self, symbol: str) -> Instrument:
        return self._repository.get_by_symbol(symbol)

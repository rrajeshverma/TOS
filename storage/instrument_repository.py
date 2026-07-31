from domain.instrument import Instrument


class InstrumentRepository:
    def __init__(self):
        self._by_symbol = {}
        self._by_security_id = {}

    def add(self, instrument: Instrument) -> None:
        self._by_symbol[instrument.symbol] = instrument
        self._by_security_id[instrument.security_id] = instrument

    def get_by_symbol(self, symbol: str) -> Instrument:
        return self._by_symbol[symbol]

    def get_by_security_id(self, security_id: str) -> Instrument:
        return self._by_security_id[security_id]

    def list_all(self) -> list[Instrument]:
        return list(self._by_symbol.values())

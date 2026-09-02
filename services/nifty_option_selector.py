"""
NIFTY option contract selection.

Selects the nearest valid NIFTY weekly option and the
nearest one-strike ITM contract for BUY_CE / BUY_PE.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from domain.instrument import Instrument
from shared.enums import Signal
from storage.instrument_repository import InstrumentRepository


class NiftyOptionSelector:
    """
    Selects the actual NIFTY option contract from the
    loaded Dhan instrument master.
    """

    def __init__(
        self,
        instrument_repository: InstrumentRepository,
    ) -> None:
        self._repository = instrument_repository

    def select(
        self,
        *,
        underlying_price: Decimal,
        signal: Signal,
        as_of: datetime,
    ) -> Instrument:
        if underlying_price <= 0:
            raise ValueError("Underlying price must be greater than zero.")

        if signal not in (Signal.BUY_CE, Signal.BUY_PE):
            raise ValueError(
                f"Unsupported option signal: {signal}",
            )

        candidates = [
            instrument
            for instrument in self._repository.list_all()
            if instrument.is_nifty_option
            and instrument.expiry is not None
            and instrument.expiry >= as_of
        ]

        if not candidates:
            raise LookupError(
                "No valid NIFTY option contracts available.",
            )

        # The earliest expiry in the instrument master is the
        # nearest valid weekly expiry for the strategy.
        nearest_expiry = min(
            instrument.expiry for instrument in candidates if instrument.expiry is not None
        )

        expiry_candidates = [
            instrument for instrument in candidates if instrument.expiry == nearest_expiry
        ]

        if signal == Signal.BUY_CE:
            itm = [
                instrument
                for instrument in expiry_candidates
                if instrument.option_type == "CE"
                and instrument.strike is not None
                and instrument.strike < underlying_price
            ]

            if not itm:
                raise LookupError(
                    "No ITM NIFTY CE strike available.",
                )

            # Nearest strike below underlying = 1 strike ITM.
            return max(
                itm,
                key=lambda instrument: instrument.strike,
            )

        itm = [
            instrument
            for instrument in expiry_candidates
            if instrument.option_type == "PE"
            and instrument.strike is not None
            and instrument.strike > underlying_price
        ]

        if not itm:
            raise LookupError(
                "No ITM NIFTY PE strike available.",
            )

        # Nearest strike above underlying = 1 strike ITM.
        return min(
            itm,
            key=lambda instrument: instrument.strike,
        )

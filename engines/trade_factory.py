"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Factory
Version     : 1.0.0
Author      : Rajesh Varma
Description : Creates Trade domain objects from
              approved Risk evaluations.
=========================================================
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from config.risk import (
    DEFAULT_NIFTY_QTY,
    RISK_REWARD_RATIO,
)
from domain.risk import Risk
from domain.trade import Trade
from shared.enums import TradeStatus
from shared.logger import get_logger
from utils.id_generator import generate_trade_id


class TradeFactory:
    """
    Creates immutable Trade objects.
    """

    def __init__(self) -> None:

        self._logger = get_logger(__name__)

    def create(
        self,
        risk: Risk,
        entry_price: Decimal,
        stop_loss: Decimal,
    ) -> Trade:

        if not risk.is_approved:
            raise ValueError("Cannot create Trade from rejected Risk.")

        risk_points = abs(entry_price - stop_loss)

        target = entry_price + (risk_points * RISK_REWARD_RATIO)

        trade = Trade(
            trade_id=generate_trade_id(),
            risk=risk,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target=target,
            quantity=DEFAULT_NIFTY_QTY,
            entry_time=datetime.now(),
            status=TradeStatus.CREATED,
        )

        self._logger.info(
            "Trade created: %s",
            trade.trade_id,
        )

        return trade

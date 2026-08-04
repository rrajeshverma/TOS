"""
=========================================================
Trading Operating System (TOS)

Module      : Trading Pipeline
Version     : 1.0.0
Author      : Rajesh Varma
Description : Orchestrates the end-to-end trading flow.
=========================================================
"""

from __future__ import annotations


class TradingPipeline:
    """
    Coordinates the complete trading workflow.
    """

    def __init__(
        self,
        market_engine,
        indicator_engine,
        decision_engine,
        trade_quality_engine,
        risk_engine,
        position_sizing_engine,
        trade_planning_engine,
        trade_management_engine,
    ):
        self._market_engine = market_engine
        self._indicator_engine = indicator_engine
        self._decision_engine = decision_engine
        self._trade_quality_engine = trade_quality_engine
        self._risk_engine = risk_engine
        self._position_sizing_engine = position_sizing_engine
        self._trade_planning_engine = trade_planning_engine
        self._trade_management_engine = trade_management_engine

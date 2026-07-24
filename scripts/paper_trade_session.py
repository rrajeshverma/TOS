"""
TOS Paper Trading Session Runner.

Operator entry point for running a paper trading session.
"""

import sys
from datetime import datetime, time
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent),
)

from market.trading_session import TradingSession
from reporting.report_service import ReportService
from runtime.session_manager import SessionManager
from runtime.startup import Startup
from services.order_execution_adapter import OrderExecutionAdapter
from services.paper_trade_runner import PaperTradeRunner


def main() -> int:

    print("=" * 45)
    print("TOS PAPER TRADING SESSION")
    print("=" * 45)

    startup = Startup()
    startup.initialize_services()

    print("Runtime       : READY")

    broker = startup.services["broker"]
    order_service = startup.services["order_service"]
    strategy_engine = startup.services["strategy_engine"]

    print(
        "Broker        :",
        "PAPER CONNECTED"
        if broker.is_connected()
        else "NOT CONNECTED",
    )

    session_manager = SessionManager()
    session_manager.open()

    trading_session = TradingSession()

    current_time = time(10, 0)

    print(
        "Market        :",
        "OPEN"
        if trading_session.is_market_open(current_time)
        else "CLOSED",
    )

    print(
        "Entry Window  :",
        "ACTIVE"
        if trading_session.is_entry_allowed(current_time)
        else "INACTIVE",
    )

    adapter = OrderExecutionAdapter(
        broker=broker,
        order_service=order_service,
    )

    runner = PaperTradeRunner(
        strategy_engine=strategy_engine,
        broker=broker,
        order_execution_adapter=adapter,
    )

    result = runner.run()

    print()
    print("Signal        :", result["signal"])
    print("Trade ID      :", result["trade_id"])
    print("Order ID      :", result["order_id"])
    print("Position ID   :", result["position_id"])

    report_service = ReportService()

    report = report_service.generate(
        title="TOS Paper Trading Session Report",
        summary={
            "status": "COMPLETED",
            "trade": result["trade_id"],
        },
        metadata={
            "generated": datetime.now(),
        },
    )

    print()
    print("Report        : GENERATED")
    print("Status        :", report.summary["status"])

    session_manager.close()

    print("Session       :", session_manager.status.upper())

    print("=" * 45)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
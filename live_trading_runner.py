import random
import time

from execution.order_poller import OrderPoller
from paper.paper_order_service import PaperOrderService
from paper.paper_position_book import PaperPositionBook
from portfolio.trade_history import TradeHistory
from services.position_manager import PositionManager
from strategy.simple_strategy import SimpleStrategy

trade_history = TradeHistory()


def main():
    print("🔥 LIVE TRADING RUNNER STARTED")

    order_service = PaperOrderService()
    position_book = PaperPositionBook()
    position_manager = PositionManager()
    strategy = SimpleStrategy()
    price = 100
    active_order = None
    cooldown = 0

    try:
        print("🚀 Starting OrderPoller...")

        poller = OrderPoller(
            order_service=order_service,
            position_manager=position_manager,
            position_book=position_book,
        )

        poller.trade_history = trade_history  # 🔥 IMPORTANT

        poller.start()

        print("🧪 Submitting test order...")

        order_id = order_service.submit(
            {
                "symbol": "NIFTY",
                "qty": 1,
                "side": "BUY",
            }
        )

        print(f"✅ Order submitted: {order_id}")

        while True:
            print("⏳ System running...")

            for position_id, data in list(position_book.get_positions().items()):
                position = data["position"]

                if position.is_closed:
                    continue

                # simulate price movement
                current = position.last_traded_price + random.randint(-2, 2)
                entry = data["entry_price"]

                pnl = (current - entry) * data["quantity"]

                print(f"💰 {position_id} PnL: {pnl}")

                # simulate market price
                price += random.randint(-3, 3)

                signal = strategy.should_enter(price)

                # 🚫 BLOCK if order already placed
                if active_order is not None:
                    continue

                # 🚫 BLOCK if ANY open position exists
                has_open_position = any(
                    not data["position"].is_closed
                    for data in position_book.get_positions().values()
                )

                if has_open_position:
                    continue

                # 🚫 cooldown
                if cooldown > 0:
                    cooldown -= 1
                    continue

                # ✅ allow entry
                if signal:
                    print(f"📢 SIGNAL: {signal} @ {price}")

                    order_id = order_service.submit(
                        {
                            "symbol": "NIFTY",
                            "qty": 1,
                            "side": signal,
                        }
                    )

                    active_order = order_id  # 🔥 IMPORTANT

                    print(f"✅ Order submitted: {order_id}")

                # store max profit per position
                if not hasattr(position, "max_profit"):
                    position.max_profit = 0

                    side = position.order["request"].get("side", "BUY")

                    if side == "BUY":
                        pnl = current - entry
                    else:
                        pnl = entry - current

                    # 🔥 track highest profit
                    print(f"📌 {position_id} | Side: {side} | Entry: {entry} | Current: {current}")

                    TRAIL = 2  # points

                    # 🔥 Trailing Stop Loss
                    if position.max_profit > 0 and pnl <= position.max_profit - TRAIL:
                        print(f"🔁 TRAILING SL HIT → EXIT {position_id}")

                        trade = position_book.close_position(
                            position_id, exit_price=current, reason="TRAILING_SL"
                        )

                        if trade:
                            trade_history.record_trade(trade)

                        continue

                # -----------------------------------
                # 🎯 TARGET / SL LOGIC
                # -----------------------------------
                # TARGET
                if pnl >= 3:
                    print(f"🎯 TARGET HIT → EXIT {position_id}")

                    trade = position_book.close_position(
                        position_id, exit_price=current, reason="TARGET"
                    )

                    if trade:
                        trade_history.record_trade(trade)

                # STOP LOSS
                elif pnl <= -2.0:
                    print(f"🛑 STOP LOSS HIT → EXIT {position_id}")

                    trade = position_book.close_position(
                        position_id, exit_price=current, reason="STOP_LOSS"
                    )

                    if trade:
                        trade_history.record_trade(trade)

                # TRAILING SL
                elif position.max_profit > 0 and pnl <= position.max_profit - 1:
                    print(f"🔁 TRAILING SL HIT → EXIT {position_id}")

                    trade = position_book.close_position(
                        position_id, exit_price=current, reason="TRAILING_SL"
                    )

                    if trade:
                        trade_history.record_trade(trade)

            # 📊 show performance
            summary = trade_history.summary()
            print(f"📊 Summary: {summary}")

            time.sleep(2)

    except Exception as e:
        print(f"❌ Error in runner: {e}")


if __name__ == "__main__":
    main()

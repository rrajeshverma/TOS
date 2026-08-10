from collections import deque
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeEvent:
    symbol: str
    side: str  # BUY / SELL
    qty: int
    price: float
    timestamp: datetime
    order_id: str


class TradeLedger:
    def __init__(self):
        self.trades = []
        self.open_positions = deque()  # FIFO
        self.realized_pnl = 0.0

    def record_trade(self, trade: TradeEvent):
        self.trades.append(trade)

        if trade.side == "BUY":
            self.open_positions.append([trade.qty, trade.price])

        elif trade.side == "SELL":
            qty_to_match = trade.qty

            if not self.open_positions:
                raise ValueError("No position to sell")

            while qty_to_match > 0:
                if not self.open_positions:
                    raise ValueError("Sell quantity exceeds position")

                buy_qty, buy_price = self.open_positions[0]

                matched_qty = min(qty_to_match, buy_qty)

                pnl = (trade.price - buy_price) * matched_qty
                self.realized_pnl += pnl

                buy_qty -= matched_qty
                qty_to_match -= matched_qty

                if buy_qty == 0:
                    self.open_positions.popleft()
                else:
                    self.open_positions[0][0] = buy_qty

    def get_unrealized_pnl(self, current_price: float):
        pnl = 0.0
        for qty, price in self.open_positions:
            pnl += (current_price - price) * qty
        return pnl

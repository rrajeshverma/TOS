import time


class PaperPositionBook:
    def __init__(self):
        # Legacy execution/live position storage.
        self._positions = {}

        # Paper trading pipeline position storage.
        self._paper_positions = {}

    # -----------------------------------
    # PAPER: RECORD TRADE
    # -----------------------------------
    def record(self, trade):
        if trade is None:
            raise ValueError("trade cannot be None")

        symbol = trade["symbol"]
        side = trade["side"]
        quantity = trade["quantity"]
        price = trade["price"]

        signed_quantity = quantity if side == "BUY" else -quantity

        position = self._paper_positions.get(symbol)

        if position is None:
            position = {
                "symbol": symbol,
                "quantity": signed_quantity,
                "price": price,
            }
            self._paper_positions[symbol] = position
        else:
            position["quantity"] += signed_quantity
            position["price"] = price

        return position

    # -----------------------------------
    # PAPER: GET POSITION
    # -----------------------------------
    def get(self, symbol):
        return self._paper_positions.get(symbol)

    # -----------------------------------
    # PAPER: LIST POSITIONS
    # -----------------------------------
    def positions(self):
        return list(self._paper_positions.values())

    # -----------------------------------
    # LIVE/EXECUTION: ADD POSITION
    # -----------------------------------
    def add_position(self, position_id, position):
        self._positions[position_id] = {
            "position": position,
            "entry_price": position.average_price,
            "quantity": position.quantity,
            "entry_time": time.time(),
        }

    # -----------------------------------
    # LIVE/EXECUTION: GET POSITIONS
    # -----------------------------------
    def get_positions(self):
        return self._positions

    # -----------------------------------
    # LEGACY: CALCULATE TOTAL PnL
    # -----------------------------------
    def calculate_pnl(self):
        total_pnl = 0

        for data in self._positions.values():
            position = data["position"]
            entry_price = data["entry_price"]
            qty = data["quantity"]

            current_price = position.last_traded_price

            pnl = (current_price - entry_price) * qty
            total_pnl += pnl

        return total_pnl

    # -----------------------------------
    # LIVE/EXECUTION: CLOSE POSITION
    # -----------------------------------
    def close_position(self, position_id, exit_price=None, reason="UNKNOWN"):
        data = self._positions.pop(position_id, None)

        if not data:
            return None

        position = data["position"]
        entry_price = data["entry_price"]
        qty = data["quantity"]

        if exit_price is None:
            exit_price = position.last_traded_price

        pnl = (exit_price - entry_price) * qty

        trade = {
            "position_id": position_id,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "quantity": qty,
            "pnl": pnl,
            "reason": reason,
        }

        print(f"📕 Position closed: {position_id} | PnL: {pnl}")

        return trade

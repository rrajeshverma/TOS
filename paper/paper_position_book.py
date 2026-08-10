import time


class PaperPositionBook:
    def __init__(self):
        self.positions = {}

    # -----------------------------------
    # ADD POSITION
    # -----------------------------------
    def add_position(self, position_id, position):
        self.positions[position_id] = {
            "position": position,
            "entry_price": position.average_price,
            "quantity": position.quantity,
            "entry_time": time.time(),
        }

    # -----------------------------------
    # GET POSITIONS
    # -----------------------------------
    def get_positions(self):
        return self.positions

    # -----------------------------------
    # CALCULATE TOTAL PnL
    # -----------------------------------
    def calculate_pnl(self):
        total_pnl = 0

        for data in self.positions.values():
            position = data["position"]
            entry_price = data["entry_price"]
            qty = data["quantity"]

            current_price = position.last_traded_price

            pnl = (current_price - entry_price) * qty
            total_pnl += pnl

        return total_pnl

    # -----------------------------------
    # CLOSE POSITION
    # -----------------------------------
    def close_position(self, position_id, exit_price=None, reason="UNKNOWN"):
        data = self.positions.pop(position_id, None)

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
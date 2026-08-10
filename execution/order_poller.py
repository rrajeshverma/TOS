import threading
import time


class OrderPoller:
    def __init__(
        self,
        order_service,
        position_manager,
        position_book=None,
        interval=1,
    ):
        self.order_service = order_service
        self.position_manager = position_manager
        self.position_book = position_book
        self.interval = interval

        self.running = False
        self.thread = None

        # 🔥 track completed orders (avoid duplicate logs)
        self._completed = set()

    # -----------------------------------
    # THREAD CONTROL
    # -----------------------------------
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    # -----------------------------------
    # MAIN LOOP
    # -----------------------------------
    def _run(self):
        while self.running:
            try:
                self._poll()
            except Exception as e:
                print(f"[Poller Error] {e}")

            time.sleep(self.interval)

    # -----------------------------------
    # CORE LOGIC
    # -----------------------------------
    def _poll(self):
        for order_id, broker_order_id in list(self.order_service._order_map.items()):
            res = self.order_service.client.get_order_status(broker_order_id)[0]

            status = res["orderStatus"]
            filled_qty = res["filledQty"]

            prev_filled = self.order_service._fills.get(order_id, 0)

            # -----------------------------------
            # 🔥 NEW FILL DETECTED
            # -----------------------------------
            if filled_qty > prev_filled:
                new_fill = filled_qty - prev_filled

                self._handle_partial_fill(order_id, res, new_fill)

                # update tracker
                self.order_service._fills[order_id] = filled_qty

            # -----------------------------------
            # COMPLETE (ONLY ONCE)
            # -----------------------------------
            if status == "TRADED" and order_id not in self._completed:
                print(f"[COMPLETE] {order_id}")
                self._completed.add(order_id)

                # 🔥 CLEANUP
                self._cleanup(order_id)

    # -----------------------------------
    # HANDLE FILL
    # -----------------------------------
    def _handle_partial_fill(self, order_id, res, new_fill_qty):
        print(f"[PARTIAL FILL] {order_id} -> {new_fill_qty}")

        price = res["averageTradedPrice"]

        order = self.order_service.get_internal_order(order_id)

        if order is None:
            print(f"[WARN] Order not found for {order_id}")
            return

        position = self.position_manager.open_position(
            order=order,
            quantity=new_fill_qty,
            price=price,
        )

        if self.position_book:
            self.position_book.add_position(
                position.position_id,
                position,
            )

    # -----------------------------------
    # CLEANUP
    # -----------------------------------
    def _cleanup(self, order_id):
        self.order_service._order_map.pop(order_id, None)
        self.order_service._fills.pop(order_id, None)
        self.order_service._orders.pop(order_id, None)

    def _handle_fill(self, fill):
        if not hasattr(self, "trade_ledger") or self.trade_ledger is None:
            return

        from portfolio.trade_ledger import TradeEvent

        trade = TradeEvent(
            symbol=fill.symbol,
            side=fill.side,
            qty=fill.qty,
            price=fill.price,
            timestamp=fill.timestamp,
            order_id=fill.order_id,
        )

        self.trade_ledger.record_trade(trade)

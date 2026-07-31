class PaperTradingPipeline:
    def __init__(self, order_service, position_book, portfolio):
        self.order_service = order_service
        self.position_book = position_book
        self.portfolio = portfolio

    def execute(self, trade):
        if trade is None:
            raise ValueError("trade cannot be None")

        order_id = self.order_service.submit(trade)

        self.position_book.record(trade)

        if trade["side"] == "BUY":
            self.portfolio.buy(
                trade["symbol"],
                trade["quantity"],
                trade["price"],
            )
        else:
            self.portfolio.sell(
                trade["symbol"],
                trade["quantity"],
                trade["price"],
            )

        return order_id

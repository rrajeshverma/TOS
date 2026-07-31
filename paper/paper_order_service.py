from uuid import uuid4


class PaperOrderService:
    def __init__(self):
        self.orders = {}

    def submit(self, request):
        if request is None:
            raise ValueError("request cannot be None")

        order_id = f"PAPER-{uuid4().hex[:8]}"

        self.orders[order_id] = dict(request)

        return order_id

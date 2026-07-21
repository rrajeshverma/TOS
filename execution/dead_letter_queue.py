class DeadLetterQueue:

    def __init__(self):
        self.orders = []

    def add(self, order):
        self.orders.append(order)

    def pop(self):
        if not self.orders:
            return None

        return self.orders.pop(0)
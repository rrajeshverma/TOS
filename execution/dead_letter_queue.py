class DeadLetterQueue:
    """
    Stores failed execution items for recovery.
    """

    def __init__(self):
        self.orders = []


    def add(
        self,
        order,
    ):
        self.orders.append(order)



    def pop(self):

        if not self.orders:
            return None

        return self.orders.pop(0)



    def count(self):

        return len(self.orders)



    def is_empty(self):

        return len(self.orders) == 0



    def clear(self):

        self.orders.clear()
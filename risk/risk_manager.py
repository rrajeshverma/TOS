class RiskManager:
    def __init__(self, max_position_size=100):
        self.max_position_size = max_position_size

    def validate(self, quantity):
        if quantity is None:
            return False

        if quantity <= 0:
            return False

        return quantity <= self.max_position_size

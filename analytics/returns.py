class Returns:
    def calculate(self, current_value, initial_value):
        if initial_value == 0:
            return 0.0

        return ((current_value - initial_value) / initial_value) * 100

    def cumulative_return(self, current_value, initial_value):
        return self.calculate(current_value, initial_value)

    def cagr(self, ending_value, beginning_value, years):
        if beginning_value == 0 or years <= 0:
            return 0.0

        return (((ending_value / beginning_value) ** (1 / years)) - 1) * 100

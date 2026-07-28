from __future__ import annotations


class AllocationEngine:
    """
    Manages portfolio capital allocation.

    Supports:
    1. Direct strategy allocation:
       AllocationEngine(100000)
       allocate("NIFTY", 20000)

    2. Percentage based allocation:
       AllocationEngine()
       allocate(
           capital=100000,
           allocations={
               "NIFTY": 50,
           },
       )
    """

    def __init__(
        self,
        capital: float = 0,
    ) -> None:

        if capital < 0:
            raise ValueError(
                "Capital cannot be negative"
            )

        self.capital = capital
        self.allocations = {}


    def allocate(
        self,
        strategy=None,
        amount=None,
        capital=None,
        allocations=None,
    ):
        """
        Allocate capital.

        Supports both allocation styles.
        """

        # Percentage allocation mode
        if allocations is not None:

            if capital is None:
                capital = self.capital

            if capital < 0:
                raise ValueError(
                    "Capital cannot be negative"
                )

            total_percentage = sum(
                allocations.values()
            )

            if total_percentage > 100:
                raise ValueError(
                    "Allocation cannot exceed 100%"
                )

            result = {}

            allocated_amount = 0

            for name, percentage in allocations.items():

                allocation_amount = (
                    capital * percentage / 100
                )

                result[name] = allocation_amount
                allocated_amount += allocation_amount

            result["cash_reserve"] = (
                capital - allocated_amount
            )

            return result


        # Strategy allocation mode

        if amount is None:
            return 0

        if amount < 0:
            amount = 0


        remaining = (
            self.capital
            - self.total_allocated()
        )

        if amount > remaining:
            amount = remaining


        self.allocations[strategy] = amount

        return amount


    def get_allocation(
        self,
        strategy: str,
    ):

        return self.allocations.get(
            strategy,
            0,
        )


    def remove_allocation(
        self,
        strategy: str,
    ):

        self.allocations.pop(
            strategy,
            None,
        )


    def total_allocated(self):

        return sum(
            self.allocations.values()
        )


    def remaining_capital(self):

        return (
            self.capital
            - self.total_allocated()
        )


    def summary(self):

        return {
            "capital": self.capital,
            "allocated": self.total_allocated(),
            "remaining": self.remaining_capital(),
            "allocations": self.allocations,
        }
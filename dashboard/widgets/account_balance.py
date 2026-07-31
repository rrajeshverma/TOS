from dataclasses import dataclass


@dataclass
class AccountBalanceWidget:
    balance: float = 0.0
    available_margin: float = 0.0

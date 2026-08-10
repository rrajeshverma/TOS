import csv
from typing import ClassVar


class CSVTradeExporter:
    HEADER: ClassVar[list[str]] = ["symbol", "entry", "exit", "qty", "pnl"]

    def export(self, trades, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(self.HEADER)

            for trade in trades:
                writer.writerow(
                    [
                        trade["symbol"],
                        trade["entry"],
                        trade["exit"],
                        trade["qty"],
                        trade["pnl"],
                    ]
                )

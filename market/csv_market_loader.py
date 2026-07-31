import csv


class CSVMarketLoader:
    def load(self, filename):
        ticks = []

        with open(filename, newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                ticks.append(
                    {
                        "symbol": row["symbol"],
                        "price": float(row["price"]),
                        "volume": int(row["volume"]),
                    }
                )

        return ticks

import csv
from pathlib import Path


class InstrumentProvider:
    def __init__(self):
        self.file = Path("data/instruments/dhan_scrip_master.csv")

    def load(self):
        with open(self.file, newline="") as f:
            reader = csv.reader(f)
            return list(reader)

    def get_nifty_index(self):
        data = self.load()

        for row in data:
            # NSE Index NIFTY 50
            if row[5] == "NIFTY" and row[0] == "NSE":
                return row

        return None

    def get_nifty_options(self, strike, option_type):
        data = self.load()

        results = []

        for row in data:
            try:
                symbol = row[5]

                if "NIFTY" in symbol and option_type in symbol and str(strike) in symbol:
                    results.append(row)

            except Exception:
                continue

        return results

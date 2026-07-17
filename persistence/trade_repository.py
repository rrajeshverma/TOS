import sqlite3

class TradeRepository:
    def __init__(self, database: str):
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                price REAL NOT NULL,
                quantity REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def save(self, trade: dict) -> None:
        status = trade.get("status", "OPEN")

        self.connection.execute(
            """
            INSERT INTO trades
                (symbol, side, price, quantity, status)
            VALUES
                (?, ?, ?, ?, ?)
            """,
            (
                trade["symbol"],
                trade["side"],
                trade["price"],
                trade["quantity"],
                status,
            ),
        )
        self.connection.commit()

    def get_all(self):
        rows = self.connection.execute(
            "SELECT * FROM trades"
        ).fetchall()

        return [dict(row) for row in rows]

    def get_by_id(self, trade_id: int):
        row = self.connection.execute(
            "SELECT * FROM trades WHERE id = ?",
            (trade_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    def find_by_symbol(self, symbol: str):
        rows = self.connection.execute(
            "SELECT * FROM trades WHERE symbol = ?",
            (symbol,),
        ).fetchall()

        return [dict(row) for row in rows]

    def update_status(self, trade_id: int, status: str) -> None:
        self.connection.execute(
            "UPDATE trades SET status = ? WHERE id = ?",
            (status, trade_id),
        )
        self.connection.commit()

    def delete(self, trade_id: int) -> None:
        self.connection.execute(
            "DELETE FROM trades WHERE id = ?",
            (trade_id,),
        )
        self.connection.commit()

    def find_open_trades(self):
        rows = self.connection.execute(
            "SELECT * FROM trades WHERE status = ?",
            ("OPEN",),
        ).fetchall()

        return [dict(row) for row in rows]

    def find_closed_trades(self):
        rows = self.connection.execute(
            """
            SELECT *
            FROM trades
            WHERE status = ?
            """,
            ("CLOSED",),
        ).fetchall()

        return [dict(row) for row in rows]
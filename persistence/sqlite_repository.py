import sqlite3


class SQLiteRepository:
    def __init__(self, database: str):
        self.connection = sqlite3.connect(database)

    def close(self) -> None:
        self.connection.close()
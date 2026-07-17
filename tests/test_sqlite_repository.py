import pytest
import sqlite3

from persistence.sqlite_repository import SQLiteRepository


def test_close_connection():
    repo = SQLiteRepository(":memory:")

    repo.close()

    with pytest.raises(sqlite3.ProgrammingError):
        repo.connection.execute("SELECT 1")
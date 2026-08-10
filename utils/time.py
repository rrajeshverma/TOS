from datetime import UTC, datetime


def now_utc():
    return datetime.now(UTC)

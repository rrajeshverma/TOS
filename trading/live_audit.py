"""
TOS Live Trading Audit

Tracks every live trading enable action.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LiveAuditRecord:
    operator: str
    reason: str
    timestamp: datetime


class LiveAuditLogger:
    """
    Stores live trading activation history.
    """

    def __init__(self) -> None:
        self._records: list[LiveAuditRecord] = []

    def record_enable(
        self,
        operator: str,
        reason: str,
    ) -> LiveAuditRecord:
        record = LiveAuditRecord(
            operator=operator,
            reason=reason,
            timestamp=datetime.now(),
        )

        self._records.append(record)

        return record

    @property
    def records(self) -> list[LiveAuditRecord]:
        return list(self._records)

    def count(self) -> int:
        return len(self._records)

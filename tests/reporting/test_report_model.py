from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class ReportModel:
    title: str
    generated_at: datetime
    summary: dict[str, Any] = field(default_factory=dict)
    sections: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
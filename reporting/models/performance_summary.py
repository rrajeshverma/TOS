from dataclasses import dataclass, field

from reporting.models.performance_model import PerformanceModel


@dataclass
class PerformanceSummary:
    """Aggregates trade performance and portfolio analytics."""

    trade_metrics: PerformanceModel | None = None
    portfolio_metrics: dict[str, float] = field(default_factory=dict)

from dataclasses import dataclass

from reporting.models.performance_model import PerformanceModel


@dataclass
class PerformanceReport:
    """Trading performance report."""

    performance: PerformanceModel
    summary: str = ""

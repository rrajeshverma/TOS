from dataclasses import dataclass

from reporting.models.performance_model import PerformanceModel


@dataclass
class PerformanceReport:
    """Trading performance report."""

    performance: PerformanceModel
    summary: str = ""

    def has_summary(self):
        return self.summary != ""

    def is_empty(self):
        return self.summary == ""

    def update_summary(self, summary):
        self.summary = summary

    def append_summary(self, text):
        self.summary += text

    def clear_summary(self):
        self.summary = ""

    def summary_length(self):
        return len(self.summary)

    def report_name(self):
        return "Performance Report"

    def copy(self):
        return PerformanceReport(
            performance=self.performance,
            summary=self.summary,
        )

    def to_dict(self):
        return {
            "performance": self.performance,
            "summary": self.summary,
        }

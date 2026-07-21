from datetime import datetime

from reporting.report_model import ReportModel
from reporting.report_statistics import ReportStatistics


class ReportBuilder:
    def build(self, title: str, trades: list[float]) -> ReportModel:
        summary = {
            "total_trades": ReportStatistics.trade_count(trades),
            "total_profit": ReportStatistics.total_profit(trades),
            "win_count": ReportStatistics.win_count(trades),
            "loss_count": ReportStatistics.loss_count(trades),
            "win_rate": ReportStatistics.win_rate(trades),
        }

        return ReportModel(
            title=title,
            generated_at=datetime.now(),
            summary=summary,
        )
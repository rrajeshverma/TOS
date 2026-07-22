from datetime import datetime

from reporting.report_model import ReportModel
from reporting.report_template import ReportTemplate


class ReportService:
    def __init__(self, template: ReportTemplate | None = None):
        self.template = template or ReportTemplate(name="default")

    def generate(
        self,
        title: str,
        summary: dict | None = None,
        sections: list | None = None,
        metadata: dict | None = None,
    ) -> ReportModel:
        return ReportModel(
            title=title,
            generated_at=datetime.now(),
            summary=summary or {},
            sections=sections or [],
            metadata=metadata or {},
        )

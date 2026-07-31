from pathlib import Path

from reporting.report_model import ReportModel


class HTMLReport:
    def render(self, report: ReportModel) -> str:
        rows = "\n".join(
            f"<tr><td>{key}</td><td>{value}</td></tr>"
            for key, value in report.summary.items()
        )

        summary_html = f"""
<table>
{rows}
</table>
"""

        return f"""<html>
<body>
<h1>{report.title}</h1>

{summary_html}

<p>{report.sections}</p>

<p>{report.metadata}</p>

</body>
</html>"""

    def export(self, report: ReportModel, path: str | Path) -> Path:
        output = Path(path)
        output.write_text(
            self.render(report),
            encoding="utf-8",
        )
        return output

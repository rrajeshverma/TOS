from reporting.report_model import ReportModel


class HTMLReport:
    def render(self, report: ReportModel) -> str:
        return f"""<html>
<body>
<h1>{report.title}</h1>

<p>{report.summary}</p>

<p>{report.sections}</p>

<p>{report.metadata}</p>

</body>
</html>"""
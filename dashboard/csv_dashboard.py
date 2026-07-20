import csv
import io

from dashboard.dashboard_model import DashboardModel
from dashboard.dashboard_renderer import DashboardRenderer


class CSVDashboard:
    def __init__(self):
        self.renderer = DashboardRenderer()

    def render(self, dashboard: DashboardModel) -> str:
        data = self.renderer.render(dashboard)

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["Section", "Data"])

        for key, value in data.items():
            writer.writerow([key, str(value)])

        return output.getvalue()

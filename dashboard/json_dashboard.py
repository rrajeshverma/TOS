import json

from dashboard.dashboard_model import DashboardModel
from dashboard.dashboard_renderer import DashboardRenderer


class JSONDashboard:
    def __init__(self):
        self.renderer = DashboardRenderer()

    def render(self, dashboard: DashboardModel) -> str:
        data = self.renderer.render(dashboard)
        return json.dumps(data, indent=4)
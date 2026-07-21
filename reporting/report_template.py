from dataclasses import dataclass


@dataclass(slots=True)
class ReportTemplate:
    name: str
    title: str = ""
    version: str = "1.0"
    author: str = ""
    description: str = ""

    def validate(self) -> bool:
        return True

    def render(self, context: dict) -> str:
        return ""
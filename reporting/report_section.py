from dataclasses import dataclass


@dataclass(slots=True)
class ReportSection:
    name: str
    content: str = ""

    def render(self) -> str:
        return f"<h2>{self.name}</h2>\n<p>{self.content}</p>"

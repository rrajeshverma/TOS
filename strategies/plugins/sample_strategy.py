from __future__ import annotations

from strategies.base_strategy import BaseStrategy


class SampleStrategy(BaseStrategy):
    def name(self) -> str:
        return "SAMPLE"

    def analyze(self, context):
        return context

    def generate_signal(self, context):
        return "WAIT"
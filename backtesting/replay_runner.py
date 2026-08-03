"""
Historical replay runner.

Feeds historical Market objects into the TradingRuntime.
"""

from __future__ import annotations


class ReplayRunner:
    """
    Replays historical market data through TradingRuntime.
    """

    def __init__(
        self,
        runtime,
        feed,
    ) -> None:
        self._runtime = runtime
        self._feed = feed

    def run(self) -> int:
        """
        Replay the complete historical feed.
        """

        history = []

        processed = 0
        skipped = 0

        for market in self._feed:
            history.append(market)

            try:
                self._runtime.on_market_tick(
                    market,
                    history,
                )

                processed += 1

                if processed % 100 == 0:
                    print(f"Processed {processed} candles...")

            except ValueError:
                # IndicatorEngine needs enough candles
                skipped += 1

        print("\nReplay completed")
        print(f"Processed : {processed}")
        print(f"Skipped    : {skipped}")

        return processed

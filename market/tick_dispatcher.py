from __future__ import annotations

from collections.abc import Callable


class TickDispatcher:
    """
    Dispatches market ticks to registered handlers.

    Features:
    - duplicate handler protection
    - handler failure isolation
    - dispatch result reporting
    """

    def __init__(self) -> None:
        self._handlers: list[
            Callable[[dict], None]
        ] = []


    def register(
        self,
        handler: Callable[[dict], None],
    ) -> None:

        if handler not in self._handlers:
            self._handlers.append(handler)



    def unregister(
        self,
        handler: Callable[[dict], None],
    ) -> None:

        if handler in self._handlers:
            self._handlers.remove(handler)



    def dispatch(
        self,
        tick: dict,
    ) -> dict:

        failed = 0


        for handler in self._handlers:

            try:
                handler(tick)

            except Exception:
                failed += 1


        return {
            "dispatched": True,
            "failed": failed,
        }
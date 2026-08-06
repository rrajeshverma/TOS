"""
Runtime Dashboard Widget.
"""

from dashboard.snapshots import RuntimeSnapshot


class RuntimeWidget:
    """
    Displays runtime information.
    """

    def render(
        self,
        snapshot: RuntimeSnapshot,
    ) -> str:
        return (
            "Runtime\n"
            f"Status : {snapshot.status}\n"
            f"Mode   : {snapshot.mode}\n"
            f"Running: {'YES' if snapshot.running else 'NO'}\n"
            f"Orders : {snapshot.metrics['orders_submitted']}\n"
            f"Rejects: {snapshot.metrics['orders_rejected']}\n"
            f"Guards : {snapshot.metrics['guard_blocks']}\n"
            f"Reconnects : {snapshot.metrics['reconnects']}\n"
        )

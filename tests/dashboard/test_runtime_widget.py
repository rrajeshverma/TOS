from dashboard.snapshots import RuntimeSnapshot
from dashboard.widgets.runtime_widget import RuntimeWidget


def test_runtime_widget_render():
    snapshot = RuntimeSnapshot(
        status="RUNNING",
        mode="PAPER",
        running=True,
        metrics={
            "orders_submitted": 10,
            "orders_rejected": 1,
            "guard_blocks": 2,
            "reconnects": 0,
        },
    )

    output = RuntimeWidget().render(snapshot)

    assert "RUNNING" in output
    assert "PAPER" in output
    assert "YES" in output
    assert "Orders : 10" in output
    assert "Rejects: 1" in output
    assert "Guards : 2" in output
    assert "Reconnects : 0" in output
from monitoring.alert_manager import (
    AlertManager,
)



def test_alert_manager_starts_empty():

    manager = AlertManager()


    assert (
        manager.count()
        == 0
    )



def test_raise_alert_creates_alert():

    manager = AlertManager()


    alert = manager.raise_alert(
        "BROKER_DOWN",
        "Dhan connection lost",
    )


    assert (
        alert["type"]
        == "BROKER_DOWN"
    )

    assert (
        manager.count()
        == 1
    )



def test_multiple_alerts_are_stored():

    manager = AlertManager()


    manager.raise_alert(
        "RISK",
        "Daily limit reached",
    )

    manager.raise_alert(
        "RECOVERY",
        "Session restored",
    )


    assert (
        manager.count()
        == 2
    )



def test_alert_type_can_be_found():

    manager = AlertManager()


    manager.raise_alert(
        "LATENCY",
        "High broker latency",
    )


    assert (
        manager.has_alert(
            "LATENCY"
        )
        is True
    )



def test_unknown_alert_type_returns_false():

    manager = AlertManager()


    assert (
        manager.has_alert(
            "UNKNOWN"
        )
        is False
    )



def test_clear_removes_all_alerts():

    manager = AlertManager()


    manager.raise_alert(
        "ERROR",
        "Execution failed",
    )


    manager.clear()


    assert (
        manager.count()
        == 0
    )

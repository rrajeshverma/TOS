from monitoring.broker_health_monitor import (
    BrokerHealthMonitor,
)



def test_default_health_is_unhealthy():

    monitor = BrokerHealthMonitor()


    assert (
        monitor.is_healthy
        is False
    )



def test_connected_broker_is_healthy():

    monitor = BrokerHealthMonitor()


    monitor.mark_connected(
        120.5
    )


    assert (
        monitor.is_healthy
        is True
    )



def test_latency_is_recorded():

    monitor = BrokerHealthMonitor()


    monitor.mark_connected(
        85
    )


    assert (
        monitor.latency()
        == 85
    )



def test_failure_marks_unhealthy():

    monitor = BrokerHealthMonitor()


    monitor.mark_connected(
        100
    )

    monitor.record_failure()


    assert (
        monitor.is_healthy
        is False
    )



def test_failure_count_increases():

    monitor = BrokerHealthMonitor()


    monitor.record_failure()

    monitor.record_failure()


    assert (
        monitor.failures()
        == 2
    )



def test_reset_clears_health_state():

    monitor = BrokerHealthMonitor()


    monitor.mark_connected(
        100
    )

    monitor.record_failure()


    monitor.reset()


    assert (
        monitor.is_healthy
        is False
    )

    assert (
        monitor.failures()
        == 0
    )

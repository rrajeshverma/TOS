from deployment.startup_health_check import (
    StartupHealthCheck,
)


def test_empty_startup_checks_are_not_ready():

    health = StartupHealthCheck()


    assert (
        health.is_ready()
        is False
    )



def test_all_checks_pass_startup():

    health = StartupHealthCheck()


    health.register_check(
        "config",
        True,
    )

    health.register_check(
        "environment",
        True,
    )


    assert (
        health.is_ready()
        is True
    )



def test_failed_check_blocks_startup():

    health = StartupHealthCheck()


    health.register_check(
        "config",
        True,
    )

    health.register_check(
        "broker",
        False,
    )


    assert (
        health.is_ready()
        is False
    )



def test_failed_checks_are_reported():

    health = StartupHealthCheck()


    health.register_check(
        "broker",
        False,
    )

    health.register_check(
        "monitoring",
        True,
    )


    assert (
        health.failed_checks()
        == ["broker"]
    )



def test_multiple_failed_checks_are_reported():

    health = StartupHealthCheck()


    health.register_check(
        "broker",
        False,
    )

    health.register_check(
        "recovery",
        False,
    )


    assert (
        len(
            health.failed_checks()
        )
        == 2
    )



def test_reset_clears_startup_state():

    health = StartupHealthCheck()


    health.register_check(
        "config",
        True,
    )


    health.reset()


    assert (
        health.is_ready()
        is False
    )

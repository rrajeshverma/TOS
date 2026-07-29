from deployment.deployment_smoke_test import (
    DeploymentSmokeTest,
)


def test_empty_deployment_is_not_successful():
    smoke = DeploymentSmokeTest()

    assert smoke.is_successful() is False


def test_complete_deployment_passes():
    smoke = DeploymentSmokeTest()

    smoke.register(
        "configuration",
        True,
    )

    smoke.register(
        "environment",
        True,
    )

    smoke.register(
        "dependencies",
        True,
    )

    smoke.register(
        "startup",
        True,
    )

    assert smoke.is_successful() is True


def test_failed_deployment_step_blocks_release():
    smoke = DeploymentSmokeTest()

    smoke.register(
        "configuration",
        True,
    )

    smoke.register(
        "broker",
        False,
    )

    assert smoke.is_successful() is False


def test_failed_steps_are_reported():
    smoke = DeploymentSmokeTest()

    smoke.register(
        "environment",
        False,
    )

    smoke.register(
        "startup",
        True,
    )

    assert smoke.failed_steps() == ["environment"]


def test_multiple_failures_are_reported():
    smoke = DeploymentSmokeTest()

    smoke.register(
        "broker",
        False,
    )

    smoke.register(
        "database",
        False,
    )

    assert len(smoke.failed_steps()) == 2


def test_reset_clears_deployment_state():
    smoke = DeploymentSmokeTest()

    smoke.register(
        "startup",
        True,
    )

    smoke.reset()

    assert smoke.is_successful() is False

from deployment.environment_validator import (
    EnvironmentValidator,
)



def test_valid_environment_is_accepted():

    validator = EnvironmentValidator()


    environment = {
        "TOS_MODE": "PAPER",
        "BROKER": "DHAN",
    }


    assert (
        validator.validate(
            environment
        )
        is True
    )



def test_empty_environment_is_rejected():

    validator = EnvironmentValidator()


    assert (
        validator.validate({})
        is False
    )



def test_missing_broker_is_rejected():

    validator = EnvironmentValidator()


    environment = {
        "TOS_MODE": "PAPER",
    }


    assert (
        validator.validate(
            environment
        )
        is False
    )



def test_live_without_credentials_is_unsafe():

    validator = EnvironmentValidator()


    environment = {
        "TOS_MODE": "LIVE",
        "BROKER": "DHAN",
        "LIVE_APPROVED": True,
    }


    assert (
        validator.is_production_safe(
            environment
        )
        is False
    )



def test_live_with_credentials_and_approval_is_safe():

    validator = EnvironmentValidator()


    environment = {
        "TOS_MODE": "LIVE",
        "BROKER": "DHAN",
        "ACCESS_TOKEN": "TOKEN123",
        "LIVE_APPROVED": True,
    }


    assert (
        validator.is_production_safe(
            environment
        )
        is True
    )



def test_paper_mode_does_not_need_credentials():

    validator = EnvironmentValidator()


    environment = {
        "TOS_MODE": "PAPER",
        "BROKER": "DHAN",
    }


    assert (
        validator.is_production_safe(
            environment
        )
        is True
    )

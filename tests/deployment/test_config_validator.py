from deployment.config_validator import (
    ConfigValidator,
)


def test_valid_configuration_is_accepted():
    validator = ConfigValidator()

    config = {
        "mode": "PAPER",
        "broker": "DHAN",
    }

    assert validator.validate(config) is True


def test_empty_configuration_is_rejected():
    validator = ConfigValidator()

    assert validator.validate({}) is False


def test_missing_required_key_is_rejected():
    validator = ConfigValidator()

    config = {
        "mode": "PAPER",
    }

    assert validator.validate(config) is False


def test_live_without_approval_is_blocked():
    validator = ConfigValidator()

    config = {
        "mode": "LIVE",
        "broker": "DHAN",
    }

    assert validator.is_live_safe(config) is False


def test_live_with_approval_is_allowed():
    validator = ConfigValidator()

    config = {
        "mode": "LIVE",
        "broker": "DHAN",
        "live_approved": True,
    }

    assert validator.is_live_safe(config) is True


def test_paper_mode_does_not_require_live_approval():
    validator = ConfigValidator()

    config = {
        "mode": "PAPER",
        "broker": "DHAN",
    }

    assert validator.is_live_safe(config) is True

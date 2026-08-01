from deployment.deployment_validator import DeploymentValidator


def test_python_version_check_returns_bool():
    assert isinstance(
        DeploymentValidator().python_version_ok(),
        bool,
    )


def test_virtual_environment_check_returns_bool():
    assert isinstance(
        DeploymentValidator().virtual_environment_active(),
        bool,
    )


def test_working_directory_check_returns_bool():
    assert isinstance(
        DeploymentValidator().working_directory_exists(),
        bool,
    )


def test_validation_summary_returns_dict():
    assert isinstance(
        DeploymentValidator().validation_summary(),
        dict,
    )


def test_summary_contains_python():
    assert "python" in DeploymentValidator().validation_summary()


def test_summary_contains_venv():
    assert "venv" in DeploymentValidator().validation_summary()


def test_summary_contains_cwd():
    assert "cwd" in DeploymentValidator().validation_summary()


def test_summary_values_are_bool():
    summary = DeploymentValidator().validation_summary()

    assert all(isinstance(v, bool) for v in summary.values())


def test_summary_has_three_entries():
    assert len(DeploymentValidator().validation_summary()) == 3


def test_validator_instantiation():
    assert DeploymentValidator() is not None

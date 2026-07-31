from operations.startup.validator import StartupValidator, ValidationResult


def test_validator_returns_validation_result():
    validator = StartupValidator()
    result = validator.run()
    assert isinstance(result, ValidationResult)


def test_validator_returns_success_by_default():
    validator = StartupValidator()
    result = validator.run()
    assert result.success is True


def test_validator_initially_has_no_checks():
    validator = StartupValidator()
    assert validator.checks == []


def test_register_single_check():
    validator = StartupValidator()
    validator.register(lambda: True)
    assert len(validator.checks) == 1


def test_register_multiple_checks():
    validator = StartupValidator()

    validator.register(lambda: True)
    validator.register(lambda: True)

    assert len(validator.checks) == 2


def test_run_with_no_checks():
    validator = StartupValidator()
    result = validator.run()
    assert result.success


def test_single_successful_check():
    validator = StartupValidator()

    validator.register(lambda: True)

    result = validator.run()

    assert result.success


def test_multiple_successful_checks():
    validator = StartupValidator()

    for _ in range(5):
        validator.register(lambda: True)

    result = validator.run()

    assert result.success


def test_single_failed_check():
    validator = StartupValidator()

    validator.register(lambda: False)

    result = validator.run()

    assert not result.success


def test_multiple_failed_checks():
    validator = StartupValidator()

    validator.register(lambda: False)
    validator.register(lambda: False)

    result = validator.run()

    assert not result.success


def test_success_and_failure():
    validator = StartupValidator()

    validator.register(lambda: True)
    validator.register(lambda: False)

    result = validator.run()

    assert not result.success


def test_validator_runs_all_checks():
    calls = []

    def check():
        calls.append(1)
        return True

    validator = StartupValidator()

    validator.register(check)
    validator.register(check)
    validator.register(check)

    validator.run()

    assert len(calls) == 3


def test_check_order_is_preserved():
    order = []

    validator = StartupValidator()

    validator.register(lambda: order.append(1) or True)
    validator.register(lambda: order.append(2) or True)

    validator.run()

    assert order == [1, 2]


def test_register_returns_none():
    validator = StartupValidator()
    assert validator.register(lambda: True) is None


def test_run_returns_validation_result():
    validator = StartupValidator()
    assert isinstance(validator.run(), ValidationResult)


def test_validator_can_be_reused():
    validator = StartupValidator()

    validator.register(lambda: True)

    assert validator.run().success
    assert validator.run().success


def test_empty_validator_multiple_runs():
    validator = StartupValidator()

    assert validator.run().success
    assert validator.run().success
    assert validator.run().success


def test_validator_accepts_callable():
    validator = StartupValidator()

    validator.register(lambda: True)

    assert callable(validator.checks[0])


def test_validation_result_success_default():
    result = ValidationResult()
    assert result.success


def test_validation_result_false():
    result = ValidationResult(success=False)
    assert not result.success

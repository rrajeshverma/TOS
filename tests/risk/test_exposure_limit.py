from risk.exposure_limit import ExposureLimitGuard


def test_guard_can_be_created():
    guard = ExposureLimitGuard()

    assert guard is not None


def test_allows_exposure_within_limit():
    guard = ExposureLimitGuard(60)

    result = guard.check(
        exposure=300000,
        capital=500000,
    )

    assert result["approved"] is True


def test_rejects_exposure_above_limit():
    guard = ExposureLimitGuard(60)

    result = guard.check(
        exposure=400000,
        capital=500000,
    )

    assert result["approved"] is False


def test_calculates_exposure_percentage():
    guard = ExposureLimitGuard(50)

    result = guard.check(
        exposure=250000,
        capital=500000,
    )

    assert result["exposure_percentage"] == 50


def test_rejects_invalid_capital():
    guard = ExposureLimitGuard()

    try:
        guard.check(
            exposure=100,
            capital=0,
        )

        assert False

    except ValueError:
        assert True


def test_custom_limit_is_used():
    guard = ExposureLimitGuard(30)

    result = guard.check(
        exposure=200000,
        capital=500000,
    )

    assert result["approved"] is False

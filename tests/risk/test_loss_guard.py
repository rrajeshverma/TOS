from risk.loss_guard import LossGuard


def test_loss_guard_can_be_created():

    guard = LossGuard(
        max_loss=10000,
    )

    assert guard is not None


def test_allows_loss_within_limit():

    guard = LossGuard(
        max_loss=10000,
    )

    result = guard.check(
        current_loss=5000,
    )

    assert result["approved"] is True


def test_rejects_loss_above_limit():

    guard = LossGuard(
        max_loss=10000,
    )

    result = guard.check(
        current_loss=15000,
    )

    assert result["approved"] is False


def test_accepts_exact_loss_limit():

    guard = LossGuard(
        max_loss=10000,
    )

    result = guard.check(
        current_loss=10000,
    )

    assert result["approved"] is True


def test_rejects_negative_loss_limit():

    try:
        LossGuard(
            max_loss=-1,
        )

        assert False

    except ValueError:
        assert True


def test_rejects_negative_current_loss():

    guard = LossGuard(
        max_loss=10000,
    )

    try:
        guard.check(
            current_loss=-100,
        )

        assert False

    except ValueError:
        assert True

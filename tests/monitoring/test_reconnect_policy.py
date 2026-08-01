from monitoring.reconnect_policy import ReconnectPolicy


def test_policy_starts_with_zero_attempts():
    assert ReconnectPolicy().attempts == 0


def test_policy_allows_retry_initially():
    assert ReconnectPolicy().can_retry()


def test_record_failure_increments_attempts():
    policy = ReconnectPolicy()

    policy.record_failure()

    assert policy.attempts == 1


def test_retry_limit_reached():
    policy = ReconnectPolicy(max_attempts=2)

    policy.record_failure()
    policy.record_failure()

    assert policy.can_retry() is False


def test_reset_clears_attempts():
    policy = ReconnectPolicy()

    policy.record_failure()
    policy.reset()

    assert policy.attempts == 0


def test_reset_restores_retry():
    policy = ReconnectPolicy(max_attempts=1)

    policy.record_failure()
    policy.reset()

    assert policy.can_retry()


def test_attempts_never_exceed_limit():
    policy = ReconnectPolicy(max_attempts=1)

    policy.record_failure()
    policy.record_failure()

    assert policy.attempts == 1


def test_multiple_resets():
    policy = ReconnectPolicy()

    policy.record_failure()
    policy.reset()
    policy.reset()

    assert policy.attempts == 0


def test_custom_retry_limit():
    policy = ReconnectPolicy(max_attempts=5)

    assert policy.can_retry()


def test_policy_is_reusable():
    policy = ReconnectPolicy()

    for _ in range(3):
        policy.record_failure()

    policy.reset()

    assert policy.attempts == 0

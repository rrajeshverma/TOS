import pytest

from execution.retry_policy import RetryPolicy


def test_success_first_attempt():
    attempts = []

    def fn():
        attempts.append(1)
        return "SUCCESS"

    policy = RetryPolicy(max_retries=3)

    assert policy.execute(fn) == "SUCCESS"
    assert len(attempts) == 1


def test_success_after_retry():
    attempts = []

    def fn():
        attempts.append(1)

        if len(attempts) < 2:
            raise RuntimeError("Temporary Error")

        return "SUCCESS"

    policy = RetryPolicy(max_retries=3)

    assert policy.execute(fn) == "SUCCESS"
    assert len(attempts) == 2


def test_retry_exhausted():
    attempts = []

    def fn():
        attempts.append(1)
        raise RuntimeError("Broker Down")

    policy = RetryPolicy(max_retries=3)

    with pytest.raises(RuntimeError):
        policy.execute(fn)

    assert len(attempts) == 3


def test_zero_retry():
    attempts = []

    def fn():
        attempts.append(1)
        raise RuntimeError()

    policy = RetryPolicy(max_retries=1)

    with pytest.raises(RuntimeError):
        policy.execute(fn)

    assert len(attempts) == 1


def test_custom_retry_count():
    policy = RetryPolicy(max_retries=5)

    assert policy.max_retries == 5

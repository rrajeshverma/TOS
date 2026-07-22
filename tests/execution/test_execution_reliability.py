import time
import pytest

from execution.retry_policy import RetryPolicy
from execution.timeout_handler import TimeoutHandler
from execution.dead_letter_queue import DeadLetterQueue


# -------------------------------
# Retry Policy Tests
# -------------------------------


def test_retry_policy_success_first_attempt():

    policy = RetryPolicy()

    result = policy.execute(
        lambda: "SUCCESS"
    )

    assert result == "SUCCESS"


def test_retry_policy_retries_after_failure():

    policy = RetryPolicy(
        max_retries=3
    )

    attempts = []

    def failing():

        attempts.append(1)
        raise Exception("failed")

    with pytest.raises(Exception):
        policy.execute(failing)

    assert len(attempts) == 3


def test_retry_policy_custom_retry_count():

    policy = RetryPolicy(
        max_retries=5
    )

    attempts = []

    def failing():

        attempts.append(1)
        raise Exception("failed")

    with pytest.raises(Exception):
        policy.execute(failing)

    assert len(attempts) == 5


def test_retry_policy_returns_after_recovery():

    policy = RetryPolicy()

    attempts = []

    def recover():

        attempts.append(1)

        if len(attempts) < 2:
            raise Exception()

        return "OK"

    assert policy.execute(recover) == "OK"

    assert len(attempts) == 2


def test_retry_policy_zero_retry():

    policy = RetryPolicy(
        max_retries=1
    )

    with pytest.raises(Exception):

        policy.execute(
            lambda: (_ for _ in ()).throw(Exception())
        )


# -------------------------------
# Timeout Tests
# -------------------------------


def test_timeout_not_reached():

    handler = TimeoutHandler(
        timeout_seconds=10
    )

    assert handler.is_timed_out(
        time.time()
    ) is False


def test_timeout_reached():

    handler = TimeoutHandler(
        timeout_seconds=1
    )

    start = time.time() - 2

    assert handler.is_timed_out(
        start
    ) is True


def test_remaining_time_positive():

    handler = TimeoutHandler(
        timeout_seconds=10
    )

    remaining = handler.remaining_time(
        time.time()
    )

    assert remaining > 0


def test_remaining_time_zero_after_timeout():

    handler = TimeoutHandler(
        timeout_seconds=1
    )

    start = time.time() - 5

    assert handler.remaining_time(
        start
    ) == 0


# -------------------------------
# Dead Letter Queue Tests
# -------------------------------


def test_dead_letter_queue_add():

    queue = DeadLetterQueue()

    queue.add(
        {
            "order": "123"
        }
    )

    assert len(queue.orders) == 1

def test_dead_letter_queue_pop():

    queue = DeadLetterQueue()

    order = {
        "order": "123"
    }

    queue.add(order)

    assert queue.pop() == order


def test_dead_letter_queue_empty_pop():

    queue = DeadLetterQueue()

    assert queue.pop() is None


def test_dead_letter_queue_fifo():

    queue = DeadLetterQueue()

    queue.add("FIRST")
    queue.add("SECOND")

    assert queue.pop() == "FIRST"
    assert queue.pop() == "SECOND"


def test_dead_letter_queue_multiple_items():

    queue = DeadLetterQueue()

    for i in range(5):
        queue.add(i)

    assert len(queue.orders) == 5
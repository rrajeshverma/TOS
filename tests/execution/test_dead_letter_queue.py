from execution.dead_letter_queue import DeadLetterQueue


def test_store_failed_order():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")

    assert len(queue.orders) == 1


def test_pop_failed_order():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")

    assert queue.pop() == "ORDER-001"


def test_queue_starts_empty():
    queue = DeadLetterQueue()

    assert queue.is_empty() is True
    assert queue.count() == 0


def test_pop_empty_queue_returns_none():
    queue = DeadLetterQueue()

    assert queue.pop() is None


def test_count_after_multiple_adds():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")
    queue.add("ORDER-002")
    queue.add("ORDER-003")

    assert queue.count() == 3


def test_fifo_order():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")
    queue.add("ORDER-002")
    queue.add("ORDER-003")

    assert queue.pop() == "ORDER-001"
    assert queue.pop() == "ORDER-002"
    assert queue.pop() == "ORDER-003"
    assert queue.pop() is None


def test_clear_queue():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")
    queue.add("ORDER-002")

    queue.clear()

    assert queue.is_empty() is True
    assert queue.count() == 0


def test_add_after_clear():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")
    queue.clear()

    queue.add("ORDER-002")

    assert queue.count() == 1
    assert queue.pop() == "ORDER-002"


def test_count_changes_after_pop():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")
    queue.add("ORDER-002")

    assert queue.count() == 2

    queue.pop()

    assert queue.count() == 1

    queue.pop()

    assert queue.count() == 0

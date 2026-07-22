from execution.dead_letter_queue import DeadLetterQueue


def test_store_failed_order():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")

    assert len(queue.orders) == 1


def test_pop_failed_order():
    queue = DeadLetterQueue()

    queue.add("ORDER-001")

    assert queue.pop() == "ORDER-001"

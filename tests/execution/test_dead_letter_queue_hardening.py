from execution.dead_letter_queue import DeadLetterQueue


def test_dead_letter_queue_add_failed_order():

    dlq = DeadLetterQueue()

    dlq.add(
        {
            "order_id": "ORD001",
            "reason": "broker timeout",
        }
    )

    assert len(dlq.orders) == 1



def test_dead_letter_queue_pop_returns_oldest():

    dlq = DeadLetterQueue()

    dlq.add(
        {
            "order_id": "ORD001"
        }
    )

    dlq.add(
        {
            "order_id": "ORD002"
        }
    )

    result = dlq.pop()

    assert result["order_id"] == "ORD001"



def test_dead_letter_queue_count():

    dlq = DeadLetterQueue()

    dlq.add(
        {
            "order_id": "ORD001"
        }
    )

    assert dlq.count() == 1

from runtime.scheduler import Scheduler


def test_scheduler_executes_task():
    scheduler = Scheduler()

    executed = []

    scheduler.run(
        lambda: executed.append(True),
    )

    assert executed == [True]


def test_scheduler_default_interval():
    scheduler = Scheduler()

    assert scheduler.interval == 1


def test_scheduler_custom_interval():
    scheduler = Scheduler(interval=5)

    assert scheduler.interval == 5

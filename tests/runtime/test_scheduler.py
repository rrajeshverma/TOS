from runtime.scheduler import Scheduler


def test_scheduler_executes_task():
    scheduler = Scheduler()

    executed = []

    scheduler.run(lambda: executed.append(True))

    assert executed == [True]


def test_scheduler_repeats_task():
    scheduler = Scheduler()

    assert scheduler.interval == 1
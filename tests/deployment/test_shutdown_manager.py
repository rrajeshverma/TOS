from deployment.shutdown_manager import (
    ShutdownManager,
)



def test_shutdown_not_started_initially():

    manager = ShutdownManager()


    assert (
        manager.is_shutdown()
        is False
    )



def test_shutdown_executes_all_steps():

    manager = ShutdownManager()


    steps = manager.execute()


    assert (
        len(steps)
        == 5
    )

    assert (
        manager.is_shutdown()
        is True
    )



def test_shutdown_steps_are_recorded():

    manager = ShutdownManager()


    manager.execute()


    assert (
        "flush_journal"
        in manager.completed_steps()
    )



def test_multiple_shutdown_calls_are_safe():

    manager = ShutdownManager()


    first = manager.execute()

    second = manager.execute()


    assert (
        first
        == second
    )



def test_reset_clears_shutdown_state():

    manager = ShutdownManager()


    manager.execute()

    manager.reset()


    assert (
        manager.is_shutdown()
        is False
    )



def test_reset_removes_completed_steps():

    manager = ShutdownManager()


    manager.execute()

    manager.reset()


    assert (
        manager.completed_steps()
        == []
    )

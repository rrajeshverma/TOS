from safety.kill_switch import KillSwitch
from safety.kill_switch_guard import KillSwitchGuard


def test_guard_allows_execution_when_inactive():
    kill_switch = KillSwitch()

    guard = KillSwitchGuard(kill_switch)

    assert guard.can_execute() is True


def test_guard_blocks_execution_when_active():
    kill_switch = KillSwitch()
    kill_switch.activate()

    guard = KillSwitchGuard(kill_switch)

    assert guard.can_execute() is False


def test_guard_allows_execution_after_deactivate():
    kill_switch = KillSwitch()
    kill_switch.activate()
    kill_switch.deactivate()

    guard = KillSwitchGuard(kill_switch)

    assert guard.can_execute() is True


def test_guard_multiple_activate_calls():
    kill_switch = KillSwitch()

    guard = KillSwitchGuard(kill_switch)

    kill_switch.activate()
    kill_switch.activate()

    assert guard.can_execute() is False


def test_guard_multiple_deactivate_calls():
    kill_switch = KillSwitch()
    kill_switch.activate()

    guard = KillSwitchGuard(kill_switch)

    kill_switch.deactivate()
    kill_switch.deactivate()

    assert guard.can_execute() is True


def test_guard_is_reusable():
    kill_switch = KillSwitch()

    guard = KillSwitchGuard(kill_switch)

    for _ in range(5):
        kill_switch.activate()
        assert guard.can_execute() is False

        kill_switch.deactivate()
        assert guard.can_execute() is True


def test_guard_instances_are_independent():
    first_switch = KillSwitch()
    second_switch = KillSwitch()

    first_guard = KillSwitchGuard(first_switch)
    second_guard = KillSwitchGuard(second_switch)

    first_switch.activate()

    assert first_guard.can_execute() is False
    assert second_guard.can_execute() is True


def test_guard_returns_boolean():
    guard = KillSwitchGuard(KillSwitch())

    assert isinstance(
        guard.can_execute(),
        bool,
    )


def test_guard_reflects_runtime_state_changes():
    kill_switch = KillSwitch()

    guard = KillSwitchGuard(kill_switch)

    assert guard.can_execute() is True

    kill_switch.activate()

    assert guard.can_execute() is False

    kill_switch.deactivate()

    assert guard.can_execute() is True


def test_guard_uses_supplied_kill_switch():
    kill_switch = KillSwitch()

    guard = KillSwitchGuard(kill_switch)

    kill_switch.activate()

    assert guard.can_execute() is False

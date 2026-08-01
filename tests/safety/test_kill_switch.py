from safety.kill_switch import KillSwitch


def test_kill_switch_starts_inactive():
    assert KillSwitch().is_active() is False


def test_activate_kill_switch():
    switch = KillSwitch()

    switch.activate()

    assert switch.is_active()


def test_deactivate_kill_switch():
    switch = KillSwitch()

    switch.activate()
    switch.deactivate()

    assert switch.is_active() is False


def test_multiple_activate_calls():
    switch = KillSwitch()

    switch.activate()
    switch.activate()

    assert switch.is_active()


def test_multiple_deactivate_calls():
    switch = KillSwitch()

    switch.deactivate()
    switch.deactivate()

    assert switch.is_active() is False


def test_activate_then_deactivate_then_activate():
    switch = KillSwitch()

    switch.activate()
    switch.deactivate()
    switch.activate()

    assert switch.is_active()


def test_instances_are_independent():
    first = KillSwitch()
    second = KillSwitch()

    first.activate()

    assert first.is_active()
    assert second.is_active() is False


def test_status_is_boolean():
    assert isinstance(
        KillSwitch().is_active(),
        bool,
    )


def test_switch_can_be_reused():
    switch = KillSwitch()

    for _ in range(5):
        switch.activate()
        switch.deactivate()

    assert switch.is_active() is False


def test_deactivate_without_activate():
    switch = KillSwitch()

    switch.deactivate()

    assert switch.is_active() is False

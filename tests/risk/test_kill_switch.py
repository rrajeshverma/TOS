from risk.kill_switch import KillSwitch


def test_enable_kill_switch():
    ks = KillSwitch()

    assert ks.is_enabled() is False

    ks.activate()

    assert ks.is_enabled() is True


def test_disable_kill_switch():
    ks = KillSwitch()

    ks.activate()
    ks.deactivate()

    assert ks.is_enabled() is False

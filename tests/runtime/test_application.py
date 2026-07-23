from runtime.application import Application


def test_application_initializes_services():
    app = Application()
    assert app.services == {}


def test_application_loads_configuration():
    app = Application()
    app.load_configuration({"mode": "paper"})
    assert app.config["mode"] == "paper"


def test_application_starts_runtime():
    app = Application()
    app.start()
    assert app.running is True


def test_application_shutdown_called():
    app = Application()
    app.start()
    app.shutdown()
    assert app.running is False

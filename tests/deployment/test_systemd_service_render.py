from deployment.service_info import ServiceInfo
from deployment.systemd_service import SystemdService


def service_text():
    return SystemdService(ServiceInfo()).render()


def test_render_contains_unit():
    assert "[Unit]" in service_text()


def test_render_contains_service():
    assert "[Service]" in service_text()


def test_render_contains_install():
    assert "[Install]" in service_text()


def test_render_contains_description():
    assert "Description=" in service_text()


def test_render_contains_exec_start():
    assert "ExecStart=python3 main.py" in service_text()


def test_render_contains_restart():
    assert "Restart=always" in service_text()


def test_render_contains_wanted_by():
    assert "WantedBy=multi-user.target" in service_text()


def test_render_contains_after_network():
    assert "After=network.target" in service_text()


def test_render_is_not_empty():
    assert service_text().strip()


def test_render_starts_with_unit():
    assert service_text().startswith("[Unit]")

from pathlib import Path

from deployment.service_info import ServiceInfo
from deployment.systemd_service import SystemdService
from deployment.systemd_writer import SystemdServiceWriter


def create_service():
    return SystemdService(ServiceInfo())


def test_writer_returns_destination(tmp_path):
    destination = tmp_path / "tos.service"

    result = SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert result == destination


def test_writer_creates_file(tmp_path):
    destination = tmp_path / "tos.service"

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert destination.exists()


def test_written_file_is_not_empty(tmp_path):
    destination = tmp_path / "tos.service"

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert destination.read_text()


def test_written_file_contains_unit(tmp_path):
    destination = tmp_path / "tos.service"

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert "[Unit]" in destination.read_text()


def test_written_file_contains_service(tmp_path):
    destination = tmp_path / "tos.service"

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert "[Service]" in destination.read_text()


def test_written_file_contains_install(tmp_path):
    destination = tmp_path / "tos.service"

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert "[Install]" in destination.read_text()


def test_written_file_contains_exec_start(tmp_path):
    destination = tmp_path / "tos.service"

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert "ExecStart=" in destination.read_text()


def test_writer_overwrites_existing_file(tmp_path):
    destination = tmp_path / "tos.service"

    destination.write_text("old")

    SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert "old" not in destination.read_text()


def test_writer_returns_path_instance(tmp_path):
    destination = tmp_path / "tos.service"

    result = SystemdServiceWriter().write(
        create_service(),
        destination,
    )

    assert isinstance(result, Path)


def test_multiple_writes_are_supported(tmp_path):
    destination = tmp_path / "tos.service"

    writer = SystemdServiceWriter()

    writer.write(create_service(), destination)
    writer.write(create_service(), destination)

    assert destination.exists()

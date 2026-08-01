from deployment.service_info import ServiceInfo
from deployment.systemd_service import SystemdService


def test_service_name():
    service = SystemdService(ServiceInfo())

    assert service.service_name == "tos.service"


def test_description():
    service = SystemdService(ServiceInfo())

    assert service.description == ServiceInfo().display_name


def test_restart_policy():
    service = SystemdService(ServiceInfo())

    assert service.restart_policy == "always"


def test_wanted_by():
    service = SystemdService(ServiceInfo())

    assert service.wanted_by == "multi-user.target"


def test_exec_start():
    service = SystemdService(ServiceInfo())

    assert service.exec_start == "python3 main.py"


def test_service_is_frozen():
    assert SystemdService.__dataclass_params__.frozen


def test_service_has_slots():
    assert hasattr(SystemdService(ServiceInfo()), "__slots__")


def test_multiple_instances_are_equal():
    assert (
        SystemdService(ServiceInfo())
        == SystemdService(ServiceInfo())
    )


def test_service_contains_service_info():
    service = SystemdService(ServiceInfo())

    assert service.service_info == ServiceInfo()


def test_service_description_not_empty():
    service = SystemdService(ServiceInfo())

    assert service.description

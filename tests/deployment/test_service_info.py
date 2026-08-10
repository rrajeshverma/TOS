from config.version import APP_NAME, BUILD, MODE, VERSION
from deployment.service_info import ServiceInfo


def test_service_name():
    assert ServiceInfo().name == APP_NAME


def test_service_version():
    assert ServiceInfo().version == VERSION


def test_service_build():
    assert ServiceInfo().build == BUILD


def test_service_mode():
    assert ServiceInfo().mode == MODE


def test_display_name_contains_app_name():
    assert APP_NAME in ServiceInfo().display_name


def test_display_name_contains_version():
    assert VERSION in ServiceInfo().display_name


def test_service_info_is_frozen():
    assert ServiceInfo().__dataclass_params__.frozen


def test_service_info_has_slots():
    assert hasattr(ServiceInfo(), "__slots__")


def test_multiple_instances_are_equal():
    assert ServiceInfo() == ServiceInfo()


def test_service_display_name():
    assert ServiceInfo().display_name == f"{APP_NAME} v{VERSION}"

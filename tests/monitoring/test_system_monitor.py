import os
import platform
import sys

from monitoring.system_monitor import SystemMonitor


def test_python_version():
    sm = SystemMonitor()
    assert sm.python_version == sys.version.split()[0]


def test_platform():
    sm = SystemMonitor()
    assert sm.platform == platform.system()


def test_platform_release():
    sm = SystemMonitor()
    assert sm.platform_release == platform.release()


def test_cpu_count():
    sm = SystemMonitor()
    assert sm.cpu_count >= 1


def test_process_id():
    sm = SystemMonitor()
    assert sm.process_id == os.getpid()


def test_dictionary():
    sm = SystemMonitor()
    data = sm.as_dict()

    assert "python_version" in data
    assert "platform" in data
    assert "cpu_count" in data


def test_repr():
    sm = SystemMonitor()
    assert "SystemMonitor" in repr(sm)


def test_platform_not_empty():
    sm = SystemMonitor()
    assert sm.platform


def test_python_version_not_empty():
    sm = SystemMonitor()
    assert sm.python_version


def test_cpu_count_integer():
    sm = SystemMonitor()
    assert isinstance(sm.cpu_count, int)

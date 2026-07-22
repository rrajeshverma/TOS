import pytest

from risk.capital_allocator import CapitalAllocator


def test_allocate_success():
    allocator = CapitalAllocator(capital=100000)

    assert allocator.allocate(10000) is True


def test_allocate_failure():
    allocator = CapitalAllocator(capital=5000)

    assert allocator.allocate(10000) is False


def test_remaining_capital():
    allocator = CapitalAllocator(capital=100000)

    allocator.allocate(25000)

    assert allocator.capital == 75000

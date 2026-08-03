"""
Tests for BaseInstrumentProvider.
"""

import pytest

from providers.base_instrument_provider import BaseInstrumentProvider


def test_cannot_instantiate_base_provider() -> None:
    """Abstract provider cannot be instantiated."""

    with pytest.raises(TypeError):
        BaseInstrumentProvider()


def test_subclass_must_implement_load() -> None:
    """Concrete subclass must implement load()."""

    class Provider(BaseInstrumentProvider):
        pass

    with pytest.raises(TypeError):
        Provider()


def test_concrete_provider_can_be_instantiated() -> None:
    """Concrete implementation is instantiable."""

    class Provider(BaseInstrumentProvider):
        def load(self):
            return []

    provider = Provider()

    assert provider.load() == []

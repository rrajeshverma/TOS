import pytest

from backtesting.historical_data_source import HistoricalDataSource


def test_historical_data_source_cannot_be_instantiated():
    with pytest.raises(TypeError):
        HistoricalDataSource()

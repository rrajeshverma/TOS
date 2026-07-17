from cache.indicator_cache import IndicatorCache


def test_store_and_get_indicator():
    cache = IndicatorCache()

    cache.set("BTCUSDT", "EMA33", 65120.45)

    assert cache.get("BTCUSDT", "EMA33") == 65120.45
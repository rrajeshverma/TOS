from cache.candle_cache import CandleCache


def test_cache_store_and_get():
    cache = CandleCache()

    candle = {
        "close": 65000,
        "volume": 1250,
    }

    cache.set("BTCUSDT", candle)

    assert cache.get("BTCUSDT") == candle


def test_get_unknown_symbol_returns_none():
    cache = CandleCache()

    assert cache.get("ETHUSDT") is None


def test_set_overwrites_existing_candle():
    cache = CandleCache()

    cache.set("BTCUSDT", {"close": 65000})
    cache.set("BTCUSDT", {"close": 65100})

    assert cache.get("BTCUSDT") == {"close": 65100}


def test_clear_removes_all_cached_candles():
    cache = CandleCache()

    cache.set("BTCUSDT", {"close": 65000})
    cache.set("ETHUSDT", {"close": 3500})

    cache.clear()

    assert cache.get("BTCUSDT") is None
    assert cache.get("ETHUSDT") is None

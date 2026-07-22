from risk.circuit_breaker import CircuitBreaker


def test_create():
    breaker = CircuitBreaker()

    assert breaker.consecutive_losses == 0
    assert breaker.daily_loss == 0


def test_add_loss():
    breaker = CircuitBreaker()

    breaker.record_loss(500)

    assert breaker.daily_loss == 500


def test_consecutive_losses():
    breaker = CircuitBreaker()

    breaker.record_loss(100)
    breaker.record_loss(100)

    assert breaker.consecutive_losses == 2


def test_record_profit():
    breaker = CircuitBreaker()

    breaker.record_profit(500)

    assert breaker.daily_loss == 0
    assert breaker.consecutive_losses == 0


def test_trip_consecutive():
    breaker = CircuitBreaker()

    breaker.record_loss(100)
    breaker.record_loss(100)
    breaker.record_loss(100)

    assert breaker.is_tripped() is True


def test_trip_daily_loss():
    breaker = CircuitBreaker()

    breaker.record_loss(5000)
    breaker.record_loss(5000)

    assert breaker.is_tripped() is True


def test_reset():
    breaker = CircuitBreaker()

    breaker.record_loss(500)
    breaker.reset()

    assert breaker.daily_loss == 0
    assert breaker.consecutive_losses == 0


def test_not_tripped():
    breaker = CircuitBreaker()

    breaker.record_loss(100)

    assert breaker.is_tripped() is False


def test_summary():
    breaker = CircuitBreaker()

    summary = breaker.summary()

    assert "daily_loss" in summary
    assert "consecutive_losses" in summary
    assert "tripped" in summary


def test_profit_resets_losses():
    breaker = CircuitBreaker()

    breaker.record_loss(100)
    breaker.record_profit(50)

    assert breaker.consecutive_losses == 0


def test_exact_daily_limit():
    breaker = CircuitBreaker()

    breaker.record_loss(10000)

    assert breaker.is_tripped() is True


def test_below_daily_limit():
    breaker = CircuitBreaker()

    breaker.record_loss(9999)

    assert breaker.is_tripped() is False


def test_four_losses():
    breaker = CircuitBreaker()

    for _ in range(4):
        breaker.record_loss(100)

    assert breaker.consecutive_losses == 4


def test_zero_profit():
    breaker = CircuitBreaker()

    breaker.record_profit(0)

    assert breaker.daily_loss == 0


def test_zero_loss():
    breaker = CircuitBreaker()

    breaker.record_loss(0)

    assert breaker.daily_loss == 0

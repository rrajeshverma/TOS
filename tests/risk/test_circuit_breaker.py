from risk.circuit_breaker import CircuitBreaker


def test_reset_clears_state():
    cb = CircuitBreaker()

    cb.record_loss(5000)
    cb.record_loss(5000)

    cb.reset()

    assert cb.daily_loss == 0
    assert cb.consecutive_losses == 0
    assert cb.is_tripped() is False


def test_summary_returns_expected_values():
    cb = CircuitBreaker()

    cb.record_loss(1000)

    summary = cb.summary()

    assert summary["daily_loss"] == 1000
    assert summary["consecutive_losses"] == 1
    assert summary["tripped"] is False

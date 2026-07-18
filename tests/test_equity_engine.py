from analytics.equity_engine import EquityEngine


def test_initial_equity():
    engine = EquityEngine(initial_capital=100000)

    assert engine.current_equity == 100000


def test_single_profit_trade():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(2500)

    assert engine.current_equity == 102500


def test_single_loss_trade():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(-1500)

    assert engine.current_equity == 98500


def test_multiple_trades():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(1000)
    engine.record_trade(-500)
    engine.record_trade(2500)

    assert engine.current_equity == 103000

def test_equity_history_starts_with_initial_capital():
    engine = EquityEngine(initial_capital=100000)

    assert engine.equity_history == [100000]


def test_equity_history_after_trades():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(1000)
    engine.record_trade(-500)
    engine.record_trade(2500)

    assert engine.equity_history == [
        100000,
        101000,
        100500,
        103000,
    ]

def test_peak_equity_initially_equals_capital():
    engine = EquityEngine(initial_capital=100000)

    assert engine.peak_equity == 100000


def test_peak_equity_updates_after_profit():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(5000)

    assert engine.peak_equity == 105000


def test_peak_equity_not_reduced_after_loss():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(5000)
    engine.record_trade(-3000)

    assert engine.current_equity == 102000
    assert engine.peak_equity == 105000


def test_peak_equity_updates_multiple_times():
    engine = EquityEngine(initial_capital=100000)

    engine.record_trade(1000)
    engine.record_trade(2000)
    engine.record_trade(-500)
    engine.record_trade(4000)

    assert engine.peak_equity == 106500
import pytest

from live.broker_session import BrokerSession
from live.order_validator import OrderValidator
from live.risk_guard import RiskGuard
from live.trade_supervisor import TradeSupervisor


# -------------------------
# Broker Session Failures
# -------------------------


def test_session_double_connect():

    session = BrokerSession()

    session.connect()
    session.connect()

    assert session.is_connected()


def test_session_disconnect_without_connect():

    session = BrokerSession()

    session.disconnect()

    assert not session.is_connected()


def test_session_reconnect_state():

    session = BrokerSession()

    session.connect()
    session.reconnect()

    assert session.is_connected()


def test_session_reset_after_connect():

    session = BrokerSession()

    session.connect()
    session.reset()

    assert session.is_connected() is False


def test_session_multiple_cycles():

    session = BrokerSession()

    for _ in range(5):
        session.connect()
        session.disconnect()

    assert not session.is_connected()


# -------------------------
# Order Validation Failures
# -------------------------


def test_validator_none_order():

    assert not OrderValidator().validate(None)


def test_validator_empty_order():

    assert not OrderValidator().validate({})


def test_validator_negative_quantity():

    order = {
        "symbol": "NIFTY",
        "quantity": -1,
        "price": 100,
    }

    assert not OrderValidator().validate(order)


def test_validator_zero_price():

    order = {
        "symbol": "NIFTY",
        "quantity": 1,
        "price": 0,
    }

    assert not OrderValidator().validate(order)


def test_validator_invalid_symbol():

    order = {
        "symbol": "",
        "quantity": 1,
        "price": 100,
    }

    assert not OrderValidator().validate(order)


# -------------------------
# Risk Protection
# -------------------------


def test_risk_multiple_losses():

    guard = RiskGuard(
        daily_loss_limit=1000
    )

    guard.record_loss(500)
    guard.record_loss(600)

    assert not guard.can_trade()


def test_risk_position_overflow():

    guard = RiskGuard(
        max_positions=1
    )

    guard.add_position()
    guard.add_position()

    assert not guard.can_open_position()


def test_risk_block_persists():

    guard = RiskGuard()

    guard.block()

    assert not guard.can_trade()


def test_risk_allow_after_block():

    guard = RiskGuard()

    guard.block()
    guard.allow()

    assert guard.can_trade()


def test_risk_loss_under_limit():

    guard = RiskGuard(
        daily_loss_limit=1000
    )

    guard.record_loss(100)

    assert guard.can_trade()


# -------------------------
# Trade Supervisor Safety
# -------------------------


def test_supervisor_initial_state():

    supervisor = TradeSupervisor()

    assert supervisor.is_running() is False


def test_supervisor_pause_state():

    supervisor = TradeSupervisor()

    supervisor.pause()

    assert supervisor.is_paused()


def test_supervisor_resume_after_pause():

    supervisor = TradeSupervisor()

    supervisor.pause()
    supervisor.resume()

    assert supervisor.is_paused() is False


def test_supervisor_restart_cycle():

    supervisor = TradeSupervisor()

    supervisor.start()
    supervisor.stop()
    supervisor.start()

    assert supervisor.is_running()


def test_supervisor_status_keys():

    supervisor = TradeSupervisor()

    status = supervisor.status()

    assert "running" in status
    assert "paused" in status
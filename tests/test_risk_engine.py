from datetime import datetime

from config.risk import MAX_DAILY_LOSS, MAX_TRADES_PER_DAY
from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from shared.enums import DecisionStatus, Signal


def create_decision():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24990,
        high=25010,
        low=24980,
        close=25000,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    return DecisionEngine().evaluate(
        market,
        indicators,
    )


def test_risk_approved():
    risk = RiskEngine().evaluate(
        decision=create_decision(),
        trades_today=0,
        daily_loss=0,
    )

    assert risk.is_approved


def test_max_trades_reached():
    risk = RiskEngine().evaluate(
        decision=create_decision(),
        trades_today=4,
        daily_loss=0,
    )

    assert not risk.is_approved


def test_daily_loss_reached():
    risk = RiskEngine().evaluate(
        decision=create_decision(),
        trades_today=0,
        daily_loss=5000,
    )

    assert not risk.is_approved


def test_blocked_decision_is_rejected():
    decision = create_decision()

    decision = decision.__class__(
        decision_id=decision.decision_id,
        timestamp=decision.timestamp,
        market=decision.market,
        indicator_set=decision.indicator_set,
        signal=decision.signal,
        status=DecisionStatus.BLOCKED,
        reasons=decision.reasons,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )

    assert not risk.is_approved
    assert "Decision not valid" in risk.reasons


def test_no_signal_is_rejected():
    decision = create_decision()

    decision = decision.__class__(
        decision_id=decision.decision_id,
        timestamp=decision.timestamp,
        market=decision.market,
        indicator_set=decision.indicator_set,
        signal=Signal.NONE,
        status=DecisionStatus.VALID,
        reasons=decision.reasons,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )

    assert not risk.is_approved
    assert "No trading signal" in risk.reasons


def test_all_failures_are_collected():
    decision = create_decision()

    decision = decision.__class__(
        decision_id=decision.decision_id,
        timestamp=decision.timestamp,
        market=decision.market,
        indicator_set=decision.indicator_set,
        signal=Signal.NONE,
        status=DecisionStatus.BLOCKED,
        reasons=decision.reasons,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=MAX_TRADES_PER_DAY,
        daily_loss=MAX_DAILY_LOSS,
    )

    assert not risk.is_approved

    assert "Decision not valid" in risk.reasons
    assert "No trading signal" in risk.reasons
    assert "Maximum trades reached" in risk.reasons
    assert "Daily loss limit reached" in risk.reasons

    assert len(risk.reasons) == 4

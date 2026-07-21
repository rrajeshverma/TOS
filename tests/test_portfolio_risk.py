from portfolio.portfolio_risk import PortfolioRisk

# ============================================================
# Maximum Risk
# ============================================================


def test_maximum_risk():
    risk = PortfolioRisk(100000, 2)

    assert risk.maximum_risk() == 2000


def test_maximum_risk_zero():
    risk = PortfolioRisk(0, 2)

    assert risk.maximum_risk() == 0


# ============================================================
# Current Risk
# ============================================================


def test_current_risk():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 500

    assert risk.remaining_risk() == 1500


def test_remaining_risk_zero():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 2000

    assert risk.remaining_risk() == 0


def test_remaining_risk_never_negative():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 5000

    assert risk.remaining_risk() == 0


# ============================================================
# Daily Loss
# ============================================================


def test_daily_loss():
    risk = PortfolioRisk(100000, 2)

    risk.daily_loss = 500

    assert risk.daily_loss == 500


def test_remaining_daily_loss():
    risk = PortfolioRisk(100000, 2)

    risk.daily_loss = 500

    assert risk.remaining_daily_loss() == 1500


def test_remaining_daily_loss_zero():
    risk = PortfolioRisk(100000, 2)

    risk.daily_loss = 2000

    assert risk.remaining_daily_loss() == 0


def test_remaining_daily_loss_never_negative():
    risk = PortfolioRisk(100000, 2)

    risk.daily_loss = 3000

    assert risk.remaining_daily_loss() == 0


# ============================================================
# Exposure
# ============================================================


def test_exposure_percent():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 500

    assert risk.exposure_percent() == 25.0


def test_exposure_percent_zero():
    risk = PortfolioRisk(100000, 2)

    assert risk.exposure_percent() == 0.0


def test_can_open_position():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 500

    assert risk.can_open_position() is True


def test_cannot_open_position():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 2000

    assert risk.can_open_position() is False


# ============================================================
# Summary
# ============================================================


def test_summary_maximum_risk():
    risk = PortfolioRisk(100000, 2)

    summary = risk.summary()

    assert summary["maximum_risk"] == 2000


def test_summary_remaining_risk():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 500

    summary = risk.summary()

    assert summary["remaining_risk"] == 1500


def test_summary_daily_loss():
    risk = PortfolioRisk(100000, 2)

    risk.daily_loss = 300

    summary = risk.summary()

    assert summary["daily_loss"] == 300


def test_summary_remaining_daily_loss():
    risk = PortfolioRisk(100000, 2)

    risk.daily_loss = 300

    summary = risk.summary()

    assert summary["remaining_daily_loss"] == 1700


def test_summary_exposure_percent():
    risk = PortfolioRisk(100000, 2)

    risk.current_risk = 500

    summary = risk.summary()

    assert summary["exposure_percent"] == 25.0


def test_summary_can_open_position():
    risk = PortfolioRisk(100000, 2)

    summary = risk.summary()

    assert summary["can_open_position"] is True

def test_exposure_percent_with_zero_maximum_risk():
    risk = PortfolioRisk(0, 2)

    assert risk.exposure_percent() == 0.0
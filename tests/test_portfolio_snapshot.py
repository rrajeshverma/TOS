from portfolio.portfolio_snapshot import PortfolioSnapshot


def test_create_snapshot():
    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=101500,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=2,
    )

    assert snapshot.cash == 100000
    assert snapshot.equity == 101500
    assert snapshot.realized_pnl == 1000
    assert snapshot.unrealized_pnl == 500
    assert snapshot.open_positions == 2


def test_snapshot_to_dict():
    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=101500,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=2,
    )

    assert snapshot.to_dict() == {
        "cash": 100000,
        "equity": 101500,
        "realized_pnl": 1000,
        "unrealized_pnl": 500,
        "open_positions": 2,
    }

# ---------- Total PnL ----------

def test_total_pnl_with_realized_and_unrealized():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    assert snapshot.total_pnl() == 1500


def test_total_pnl_realized_only():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 0, 1)

    assert snapshot.total_pnl() == 1000


def test_total_pnl_zero():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 0)

    assert snapshot.total_pnl() == 0


# ---------- Status ----------

def test_is_profitable_true():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 0, 1)

    assert snapshot.is_profitable() is True


def test_is_profitable_false():
    snapshot = PortfolioSnapshot(100000, 99000, -1000, 0, 1)

    assert snapshot.is_profitable() is False


def test_has_open_positions():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 2)

    assert snapshot.has_open_positions() is True


# ---------- Position Management ----------

def test_increment_positions():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 1)

    snapshot.increment_positions()

    assert snapshot.open_positions == 2


def test_decrement_positions():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 2)

    snapshot.decrement_positions()

    assert snapshot.open_positions == 1


def test_reset_positions():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 5)

    snapshot.reset_positions()

    assert snapshot.open_positions == 0


def test_positions_never_negative():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 0)

    snapshot.decrement_positions()

    assert snapshot.open_positions == 0


# ---------- Cash Management ----------

def test_deposit():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 0)

    snapshot.deposit(5000)

    assert snapshot.cash == 105000


def test_withdraw():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 0)

    snapshot.withdraw(25000)

    assert snapshot.cash == 75000


def test_withdraw_never_negative():
    snapshot = PortfolioSnapshot(1000, 1000, 0, 0, 0)

    snapshot.withdraw(5000)

    assert snapshot.cash == 0


# ---------- Copy ----------

def test_copy_returns_new_object():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 0, 2)

    clone = snapshot.copy()

    assert clone is not snapshot


def test_copy_preserves_values():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 500, 2)

    clone = snapshot.copy()

    assert clone.to_dict() == snapshot.to_dict()


def test_copy_is_independent():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 500, 2)

    clone = snapshot.copy()

    clone.deposit(1000)

    assert snapshot.cash == 100000
    assert clone.cash == 101000
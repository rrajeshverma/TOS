from decimal import Decimal

from services.account_synchronizer import AccountSynchronizer
from services.paper_trading_service import PaperTradingService
from services.portfolio_service import PortfolioService
from services.position_manager import PositionManager
from shared.enums import TradeStatus
from tests.helpers.domain_factory import (
    make_portfolio,
    make_trade,
)


class FakePortfolioRepository:
    def __init__(self):
        self.portfolio = None

    def get(self):
        return self.portfolio

    def save(self, portfolio):
        self.portfolio = portfolio

    def clear(self):
        self.portfolio = None

    def exists(self):
        return self.portfolio is not None


class FakeBroker:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def get_portfolio(self):
        return self.portfolio


# ---------------------------------------------------------------------
# PaperTradingService
# ---------------------------------------------------------------------


def test_execute_creates_open_position():
    service = PaperTradingService()

    position = service.execute(make_trade())

    assert position.status == TradeStatus.OPEN


def test_execute_quantity():
    service = PaperTradingService()

    position = service.execute(make_trade())

    trade = make_trade()

    position = service.execute(trade)

    assert position.quantity == trade.quantity


def test_update_price():
    service = PaperTradingService()

    position = service.execute(make_trade())

    updated = service.update_price(position, Decimal(255))

    assert updated.last_traded_price == Decimal(255)


def test_close_position():
    service = PaperTradingService()

    position = service.execute(make_trade())

    closed = service.close(position, Decimal(260))

    assert closed.status == TradeStatus.CLOSED


def test_close_sets_closed_at():
    service = PaperTradingService()

    position = service.execute(make_trade())

    closed = service.close(position, Decimal(260))

    assert closed.closed_at is not None


# ---------------------------------------------------------------------
# PositionManager
# ---------------------------------------------------------------------


def test_open_position():
    manager = PositionManager()

    position = manager.open_position(
        None,
        25,
        Decimal(100),
    )

    assert position.status == TradeStatus.OPEN


def test_update_position_price():
    manager = PositionManager()

    position = manager.open_position(
        None,
        25,
        Decimal(100),
    )

    updated = manager.update_price(
        position,
        Decimal(110),
    )

    assert updated.last_traded_price == Decimal(110)


def test_close_position_manager():
    manager = PositionManager()

    position = manager.open_position(
        None,
        25,
        Decimal(100),
    )

    closed = manager.close_position(
        position,
        Decimal(120),
    )

    assert closed.status == TradeStatus.CLOSED


def test_unrealized_pnl():
    manager = PositionManager()

    position = manager.open_position(
        None,
        10,
        Decimal(100),
    )

    updated = manager.update_price(
        position,
        Decimal(105),
    )

    assert manager.unrealized_pnl(updated) == Decimal(50)


def test_realized_pnl():
    manager = PositionManager()

    assert manager.realized_pnl(
        Decimal(100),
        Decimal(110),
        10,
    ) == Decimal(100)


def test_position_is_open():
    manager = PositionManager()

    position = manager.open_position(
        None,
        1,
        Decimal(10),
    )

    assert manager.is_position_open(position)


# ---------------------------------------------------------------------
# PortfolioService
# ---------------------------------------------------------------------


def test_portfolio_update():
    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    portfolio = make_portfolio()

    service.update(portfolio)

    assert service.exists()


def test_get_account_id():
    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    portfolio = make_portfolio()

    service.update(portfolio)

    assert service.get_account_id() == "ACC001"


def test_clear_portfolio():
    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    portfolio = make_portfolio()

    service.update(portfolio)

    service.clear()

    assert not service.exists()


# ---------------------------------------------------------------------
# AccountSynchronizer
# ---------------------------------------------------------------------


def test_account_sync():
    portfolio = make_portfolio()

    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    broker = FakeBroker(portfolio)

    sync = AccountSynchronizer(
        broker,
        service,
    )

    result = sync.sync()

    assert result.account_id == "ACC001"


def test_last_portfolio():
    portfolio = make_portfolio()

    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    broker = FakeBroker(portfolio)

    sync = AccountSynchronizer(
        broker,
        service,
    )

    sync.sync()

    assert sync.last_portfolio() == portfolio


def test_sync_updates_service():
    portfolio = make_portfolio()

    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    broker = FakeBroker(portfolio)

    sync = AccountSynchronizer(
        broker,
        service,
    )

    sync.sync()

    assert service.exists()


def test_multiple_syncs():
    portfolio = make_portfolio()

    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    broker = FakeBroker(portfolio)

    sync = AccountSynchronizer(
        broker,
        service,
    )

    for _ in range(5):
        sync.sync()

    assert sync.last_portfolio().account_id == "ACC001"


def test_portfolio_initially_none():
    repo = FakePortfolioRepository()

    service = PortfolioService(repo)

    broker = FakeBroker(None)

    sync = AccountSynchronizer(
        broker,
        service,
    )

    assert sync.last_portfolio() is None

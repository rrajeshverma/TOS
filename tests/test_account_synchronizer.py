from domain.portfolio import Portfolio
from services.account_synchronizer import AccountSynchronizer
from services.portfolio_service import PortfolioService
from storage.portfolio_repository import PortfolioRepository
from unittest.mock import Mock


class FakeBroker:
    def get_portfolio(self):
        return Portfolio(
            account_id="ACC123",
            cash=100000.0,
            available_margin=80000.0,
            used_margin=20000.0,
            equity=100000.0,
            realized_pnl=500.0,
            unrealized_pnl=250.0,
            positions=2,
            holdings=1,
        )


def test_sync_updates_repository():
    repo = PortfolioRepository()
    service = PortfolioService(repo)
    broker = FakeBroker()

    synchronizer = AccountSynchronizer(broker, service)

    synchronizer.sync()

    portfolio = service.get_portfolio()

    assert portfolio.account_id == "ACC123"
    assert portfolio.cash == 100000.0


def test_last_portfolio():
    repo = PortfolioRepository()
    service = PortfolioService(repo)
    broker = FakeBroker()

    synchronizer = AccountSynchronizer(broker, service)

    synchronizer.sync()

    assert synchronizer.last_portfolio() == service.get_portfolio()


def test_last_portfolio_initially_none():
    repo = PortfolioRepository()
    service = PortfolioService(repo)
    broker = FakeBroker()

    synchronizer = AccountSynchronizer(
        broker,
        service,
    )

    assert synchronizer.last_portfolio() is None


def test_sync_returns_portfolio():
    repo = PortfolioRepository()
    service = PortfolioService(repo)
    broker = FakeBroker()

    synchronizer = AccountSynchronizer(
        broker,
        service,
    )

    portfolio = synchronizer.sync()

    assert portfolio.account_id == "ACC123"


def test_sync_updates_last_portfolio_reference():
    repo = PortfolioRepository()
    service = PortfolioService(repo)
    broker = FakeBroker()

    synchronizer = AccountSynchronizer(
        broker,
        service,
    )

    returned = synchronizer.sync()

    assert synchronizer.last_portfolio() is returned


def test_sync_calls_broker_once():
    broker = Mock()

    portfolio = Portfolio(
        account_id="ACC123",
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )

    broker.get_portfolio.return_value = portfolio

    repo = PortfolioRepository()
    service = PortfolioService(repo)

    synchronizer = AccountSynchronizer(
        broker,
        service,
    )

    synchronizer.sync()

    broker.get_portfolio.assert_called_once()


def test_sync_updates_portfolio_service_once():
    broker = Mock()

    portfolio = Portfolio(
        account_id="ACC123",
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )

    broker.get_portfolio.return_value = portfolio

    service = Mock()

    synchronizer = AccountSynchronizer(
        broker,
        service,
    )

    synchronizer.sync()

    service.update.assert_called_once_with(portfolio)


def test_sync_multiple_times_updates_last_portfolio():
    class Broker:
        def __init__(self):
            self.counter = 0

        def get_portfolio(self):
            self.counter += 1

            return Portfolio(
                account_id=f"ACC{self.counter}",
                cash=100000.0,
                available_margin=80000.0,
                used_margin=20000.0,
                equity=100000.0,
                realized_pnl=500.0,
                unrealized_pnl=250.0,
                positions=2,
                holdings=1,
            )

    repo = PortfolioRepository()
    service = PortfolioService(repo)

    synchronizer = AccountSynchronizer(
        Broker(),
        service,
    )

    synchronizer.sync()
    synchronizer.sync()

    assert synchronizer.last_portfolio().account_id == "ACC2"

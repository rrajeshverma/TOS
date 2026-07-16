from domain.portfolio import Portfolio
from services.account_synchronizer import AccountSynchronizer
from services.portfolio_service import PortfolioService
from storage.portfolio_repository import PortfolioRepository


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
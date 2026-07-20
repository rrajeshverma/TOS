from domain.portfolio import Portfolio
from storage.portfolio_repository import PortfolioRepository
from services.portfolio_service import PortfolioService


def sample_portfolio():
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


def test_get_portfolio():
    repo = PortfolioRepository()
    portfolio = sample_portfolio()
    repo.save(portfolio)

    service = PortfolioService(repo)

    assert service.get_portfolio() == portfolio


def test_get_account_id():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = PortfolioService(repo)

    assert service.get_account_id() == "ACC123"


def test_update_portfolio():
    repo = PortfolioRepository()
    service = PortfolioService(repo)

    portfolio = sample_portfolio()
    service.update(portfolio)

    assert repo.get() == portfolio


def test_clear_portfolio():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = PortfolioService(repo)

    service.clear()

    assert repo.get() is None


def test_exists():
    repo = PortfolioRepository()
    service = PortfolioService(repo)

    assert service.exists() is False

    service.update(sample_portfolio())

    assert service.exists() is True

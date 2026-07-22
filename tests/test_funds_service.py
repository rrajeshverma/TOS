from domain.portfolio import Portfolio
from services.funds_service import FundsService
from storage.portfolio_repository import PortfolioRepository


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


def test_get_cash():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = FundsService(repo)

    assert service.get_cash() == 100000.0


def test_get_available_margin():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = FundsService(repo)

    assert service.get_available_margin() == 80000.0


def test_get_used_margin():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = FundsService(repo)

    assert service.get_used_margin() == 20000.0


def test_get_equity():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = FundsService(repo)

    assert service.get_equity() == 100000.0


def test_update_portfolio():
    repo = PortfolioRepository()

    service = FundsService(repo)

    portfolio = sample_portfolio()

    service.update(portfolio)

    assert repo.get() == portfolio

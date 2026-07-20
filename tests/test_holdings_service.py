from domain.portfolio import Portfolio
from storage.portfolio_repository import PortfolioRepository
from services.holdings_service import HoldingsService


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


def test_get_holdings_count():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = HoldingsService(repo)

    assert service.get_holdings_count() == 1


def test_get_positions_count():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = HoldingsService(repo)

    assert service.get_positions_count() == 2


def test_get_realized_pnl():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = HoldingsService(repo)

    assert service.get_realized_pnl() == 500.0


def test_get_unrealized_pnl():
    repo = PortfolioRepository()
    repo.save(sample_portfolio())

    service = HoldingsService(repo)

    assert service.get_unrealized_pnl() == 250.0


def test_update_portfolio():
    repo = PortfolioRepository()

    service = HoldingsService(repo)

    portfolio = sample_portfolio()

    service.update(portfolio)

    assert repo.get() == portfolio

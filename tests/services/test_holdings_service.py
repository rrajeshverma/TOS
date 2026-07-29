from domain.portfolio import Portfolio
from services.holdings_service import HoldingsService
from storage.portfolio_repository import PortfolioRepository


def create_portfolio():
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


def test_get_holdings_count_empty_repository():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    assert service.get_holdings_count() == 0


def test_get_positions_count_empty_repository():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    assert service.get_positions_count() == 0


def test_get_realized_pnl_empty_repository():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    assert service.get_realized_pnl() == 0.0


def test_get_unrealized_pnl_empty_repository():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    assert service.get_unrealized_pnl() == 0.0


def test_update_saves_portfolio():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    portfolio = create_portfolio()

    service.update(portfolio)

    assert repo.get() == portfolio


def test_get_holdings_count():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    portfolio = create_portfolio()

    service.update(portfolio)

    assert service.get_holdings_count() == 1


def test_get_positions_count():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    portfolio = create_portfolio()

    service.update(portfolio)

    assert service.get_positions_count() == 2


def test_get_realized_pnl():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    portfolio = create_portfolio()

    service.update(portfolio)

    assert service.get_realized_pnl() == 500.0


def test_get_unrealized_pnl():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    portfolio = create_portfolio()

    service.update(portfolio)

    assert service.get_unrealized_pnl() == 250.0


def test_update_overwrites_previous_portfolio():
    repo = PortfolioRepository()
    service = HoldingsService(repo)

    first = create_portfolio()

    second = Portfolio(
        account_id="ACC999",
        cash=200000.0,
        available_margin=150000.0,
        used_margin=50000.0,
        equity=200000.0,
        realized_pnl=1000.0,
        unrealized_pnl=750.0,
        positions=5,
        holdings=3,
    )

    service.update(first)
    service.update(second)

    assert service.get_holdings_count() == 3
    assert service.get_positions_count() == 5
    assert service.get_realized_pnl() == 1000.0
    assert service.get_unrealized_pnl() == 750.0

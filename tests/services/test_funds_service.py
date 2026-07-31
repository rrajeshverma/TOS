from domain.portfolio import Portfolio
from services.funds_service import FundsService
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


def test_get_cash_empty_repository():
    repo = PortfolioRepository()
    service = FundsService(repo)

    assert service.get_cash() == 0.0


def test_get_available_margin_empty_repository():
    repo = PortfolioRepository()
    service = FundsService(repo)

    assert service.get_available_margin() == 0.0


def test_get_used_margin_empty_repository():
    repo = PortfolioRepository()
    service = FundsService(repo)

    assert service.get_used_margin() == 0.0


def test_get_equity_empty_repository():
    repo = PortfolioRepository()
    service = FundsService(repo)

    assert service.get_equity() == 0.0


def test_update_saves_portfolio():
    repo = PortfolioRepository()
    service = FundsService(repo)

    portfolio = create_portfolio()

    service.update(portfolio)

    assert repo.get() == portfolio


def test_get_cash():
    repo = PortfolioRepository()
    service = FundsService(repo)

    service.update(create_portfolio())

    assert service.get_cash() == 100000.0


def test_get_available_margin():
    repo = PortfolioRepository()
    service = FundsService(repo)

    service.update(create_portfolio())

    assert service.get_available_margin() == 80000.0


def test_get_used_margin():
    repo = PortfolioRepository()
    service = FundsService(repo)

    service.update(create_portfolio())

    assert service.get_used_margin() == 20000.0


def test_get_equity():
    repo = PortfolioRepository()
    service = FundsService(repo)

    service.update(create_portfolio())

    assert service.get_equity() == 100000.0


def test_update_overwrites_previous_portfolio():
    repo = PortfolioRepository()
    service = FundsService(repo)

    first = create_portfolio()

    second = Portfolio(
        account_id="ACC999",
        cash=250000.0,
        available_margin=180000.0,
        used_margin=70000.0,
        equity=250000.0,
        realized_pnl=1500.0,
        unrealized_pnl=900.0,
        positions=4,
        holdings=2,
    )

    service.update(first)
    service.update(second)

    assert service.get_cash() == 250000.0
    assert service.get_available_margin() == 180000.0
    assert service.get_used_margin() == 70000.0
    assert service.get_equity() == 250000.0

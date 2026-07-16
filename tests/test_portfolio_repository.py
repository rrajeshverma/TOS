from domain.portfolio import Portfolio
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


def test_save_and_get_portfolio():
    repo = PortfolioRepository()
    portfolio = sample_portfolio()

    repo.save(portfolio)

    result = repo.get()

    assert result == portfolio


def test_repository_exists():
    repo = PortfolioRepository()

    assert repo.exists() is False

    repo.save(sample_portfolio())

    assert repo.exists() is True


def test_clear_repository():
    repo = PortfolioRepository()

    repo.save(sample_portfolio())

    repo.clear()

    assert repo.get() is None
    assert repo.exists() is False
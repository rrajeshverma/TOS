from domain.portfolio import Portfolio
from storage.portfolio_repository import PortfolioRepository


def create_portfolio(account_id="ACC001"):
    return Portfolio(
        account_id=account_id,
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )


def test_repository_starts_empty():
    repository = PortfolioRepository()

    assert repository.get() is None
    assert repository.exists() is False


def test_save_and_get():
    repository = PortfolioRepository()

    portfolio = create_portfolio()

    repository.save(portfolio)

    assert repository.get() is portfolio
    assert repository.exists() is True


def test_clear_repository():
    repository = PortfolioRepository()

    repository.save(create_portfolio())

    repository.clear()

    assert repository.get() is None
    assert repository.exists() is False


def test_clear_empty_repository():
    repository = PortfolioRepository()

    repository.clear()

    assert repository.get() is None
    assert repository.exists() is False


def test_save_overwrites_previous_portfolio():
    repository = PortfolioRepository()

    first = create_portfolio("ACC001")
    second = create_portfolio("ACC002")

    repository.save(first)
    repository.save(second)

    assert repository.get() is second
    assert repository.get().account_id == "ACC002"


def test_get_returns_same_instance():
    repository = PortfolioRepository()

    portfolio = create_portfolio()

    repository.save(portfolio)

    assert repository.get() is portfolio


def test_exists_after_multiple_operations():
    repository = PortfolioRepository()

    assert repository.exists() is False

    repository.save(create_portfolio())

    assert repository.exists() is True

    repository.clear()

    assert repository.exists() is False

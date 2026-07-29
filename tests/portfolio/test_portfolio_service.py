from unittest.mock import Mock

from domain.portfolio import Portfolio
from services.portfolio_service import PortfolioService


def create_portfolio():
    return Portfolio(
        account_id="ACC001",
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
    repository = Mock()

    portfolio = create_portfolio()

    repository.get.return_value = portfolio

    service = PortfolioService(repository)

    assert service.get_portfolio() is portfolio


def test_get_portfolio_none():
    repository = Mock()

    repository.get.return_value = None

    service = PortfolioService(repository)

    assert service.get_portfolio() is None


def test_get_account_id():
    repository = Mock()

    repository.get.return_value = create_portfolio()

    service = PortfolioService(repository)

    assert service.get_account_id() == "ACC001"


def test_get_account_id_none():
    repository = Mock()

    repository.get.return_value = None

    service = PortfolioService(repository)

    assert service.get_account_id() is None


def test_update():
    repository = Mock()

    service = PortfolioService(repository)

    portfolio = create_portfolio()

    service.update(portfolio)

    repository.save.assert_called_once_with(portfolio)


def test_clear():
    repository = Mock()

    service = PortfolioService(repository)

    service.clear()

    repository.clear.assert_called_once()


def test_exists_true():
    repository = Mock()

    repository.exists.return_value = True

    service = PortfolioService(repository)

    assert service.exists() is True


def test_exists_false():
    repository = Mock()

    repository.exists.return_value = False

    service = PortfolioService(repository)

    assert service.exists() is False


def test_get_portfolio_calls_repository_once():
    repository = Mock()

    repository.get.return_value = create_portfolio()

    service = PortfolioService(repository)

    service.get_portfolio()

    repository.get.assert_called_once()


def test_get_account_id_calls_repository_once():
    repository = Mock()

    repository.get.return_value = create_portfolio()

    service = PortfolioService(repository)

    service.get_account_id()

    repository.get.assert_called_once()


def test_exists_calls_repository_once():
    repository = Mock()

    repository.exists.return_value = True

    service = PortfolioService(repository)

    service.exists()

    repository.exists.assert_called_once()


def test_clear_does_not_call_save():
    repository = Mock()

    service = PortfolioService(repository)

    service.clear()

    repository.save.assert_not_called()


def test_update_does_not_call_clear():
    repository = Mock()

    service = PortfolioService(repository)

    service.update(create_portfolio())

    repository.clear.assert_not_called()

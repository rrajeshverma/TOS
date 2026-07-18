from portfolio.strategy_validator import StrategyValidator


class DummyStrategy:
    def execute(self):
        return "BUY"


class InvalidStrategy:
    pass


def test_create_validator():
    validator = StrategyValidator()

    assert validator is not None


def test_valid_name():
    validator = StrategyValidator()

    assert validator.is_valid_name("ORB")


def test_invalid_empty_name():
    validator = StrategyValidator()

    assert validator.is_valid_name("") is False


def test_invalid_none_name():
    validator = StrategyValidator()

    assert validator.is_valid_name(None) is False


def test_valid_strategy():
    validator = StrategyValidator()

    assert validator.is_valid_strategy(
        DummyStrategy()
    )


def test_invalid_strategy():
    validator = StrategyValidator()

    assert validator.is_valid_strategy(
        InvalidStrategy()
    ) is False


def test_validate():
    validator = StrategyValidator()

    assert validator.validate(
        "ORB",
        DummyStrategy(),
    )


def test_validate_invalid_name():
    validator = StrategyValidator()

    assert validator.validate(
        "",
        DummyStrategy(),
    ) is False


def test_validate_invalid_strategy():
    validator = StrategyValidator()

    assert validator.validate(
        "ORB",
        InvalidStrategy(),
    ) is False


def test_validate_many():
    validator = StrategyValidator()

    strategies = {
        "ORB": DummyStrategy(),
        "VWAP": DummyStrategy(),
    }

    assert validator.validate_many(
        strategies
    )


def test_validate_many_invalid():
    validator = StrategyValidator()

    strategies = {
        "ORB": DummyStrategy(),
        "VWAP": InvalidStrategy(),
    }

    assert validator.validate_many(
        strategies
    ) is False
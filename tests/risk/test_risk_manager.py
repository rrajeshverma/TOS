from risk.risk_manager import RiskManager


def test_can_create_manager():
    assert RiskManager() is not None


def test_default_max_position_size():
    manager = RiskManager()

    assert manager.max_position_size == 100


def test_accepts_small_position():
    manager = RiskManager()

    assert manager.validate(quantity=50)


def test_rejects_large_position():
    manager = RiskManager()

    assert not manager.validate(quantity=150)


def test_accepts_exact_limit():
    manager = RiskManager()

    assert manager.validate(quantity=100)


def test_rejects_zero_quantity():
    manager = RiskManager()

    assert not manager.validate(quantity=0)


def test_rejects_negative_quantity():
    manager = RiskManager()

    assert not manager.validate(quantity=-10)


def test_custom_limit():
    manager = RiskManager(max_position_size=25)

    assert manager.validate(quantity=25)


def test_custom_limit_rejects():
    manager = RiskManager(max_position_size=25)

    assert not manager.validate(quantity=26)


def test_repeatable_validation():
    manager = RiskManager()

    assert manager.validate(10) == manager.validate(10)


def test_multiple_calls():
    manager = RiskManager()

    for _ in range(10):
        assert manager.validate(50)


def test_stateless():
    manager = RiskManager()

    manager.validate(10)

    assert manager.max_position_size == 100


def test_limit_property():
    manager = RiskManager()

    assert hasattr(manager, "max_position_size")


def test_none_quantity():
    manager = RiskManager()

    assert not manager.validate(None)


def test_large_limit():
    manager = RiskManager(max_position_size=1000)

    assert manager.validate(999)

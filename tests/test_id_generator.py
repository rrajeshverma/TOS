from utils.id_generator import (
    generate_decision_id,
    generate_order_id,
    generate_position_id,
    generate_trade_id,
)


def test_generate_decision_id():
    assert generate_decision_id().startswith("D")


def test_generate_trade_id():
    assert generate_trade_id().startswith("T")


def test_generate_order_id():
    assert generate_order_id().startswith("O")


def test_generate_position_id():
    assert generate_position_id().startswith("P")


def test_ids_are_unique():
    first = generate_trade_id()
    second = generate_trade_id()

    assert first != second

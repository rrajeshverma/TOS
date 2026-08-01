from strategies.filters.confirmation_filter import (
    ConfirmationFilter,
)


def test_buy_confirmation():
    assert ConfirmationFilter().buy_allowed(
        signal_high=100,
        current_high=101,
    )


def test_buy_confirmation_equal():
    assert not ConfirmationFilter().buy_allowed(
        signal_high=100,
        current_high=100,
    )


def test_buy_confirmation_below():
    assert not ConfirmationFilter().buy_allowed(
        signal_high=100,
        current_high=99,
    )


def test_sell_confirmation():
    assert ConfirmationFilter().sell_allowed(
        signal_low=100,
        current_low=99,
    )


def test_sell_confirmation_equal():
    assert not ConfirmationFilter().sell_allowed(
        signal_low=100,
        current_low=100,
    )


def test_sell_confirmation_above():
    assert not ConfirmationFilter().sell_allowed(
        signal_low=100,
        current_low=101,
    )

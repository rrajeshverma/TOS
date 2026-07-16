from dashboard.widgets.account_balance import AccountBalanceWidget


def test_account_balance_widget_defaults():
    widget = AccountBalanceWidget()

    assert widget.balance == 0.0
    assert widget.available_margin == 0.0
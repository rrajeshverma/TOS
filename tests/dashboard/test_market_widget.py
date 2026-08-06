from dashboard.widgets.market_widget import MarketWidget


def test_market_widget_defaults():
    widget = MarketWidget()

    assert widget.session == "CLOSED"
    assert widget.symbol == "NIFTY"
    assert widget.price == 0.0
    assert widget.last_tick == "--:--:--"


def test_market_widget_custom_values():
    widget = MarketWidget(
        session="OPEN",
        symbol="BANKNIFTY",
        price=55842.35,
        last_tick="09:15:01",
    )

    assert widget.session == "OPEN"
    assert widget.symbol == "BANKNIFTY"
    assert widget.price == 55842.35
    assert widget.last_tick == "09:15:01"


def test_market_widget_render():
    widget = MarketWidget(
        session="OPEN",
        symbol="NIFTY",
        price=25124.45,
        last_tick="09:20:11",
    )

    output = widget.render()

    assert "Market" in output
    assert "OPEN" in output
    assert "25124.45" in output
    assert "09:20:11" in output

from strategies.nifty_orb import NiftyORBStrategy


def test_nifty_orb_has_name():

    strategy = NiftyORBStrategy()

    assert (
        strategy.name()
        == "NIFTY_ORB"
    )


def test_nifty_orb_can_analyze():

    strategy = NiftyORBStrategy()

    result = strategy.analyze(
        None
    )

    assert result is not None



def test_nifty_orb_generates_no_signal_without_context():

    strategy = NiftyORBStrategy()

    signal = strategy.generate_signal(
        None
    )

    assert signal is None



def test_nifty_orb_buy_signal():

    strategy = NiftyORBStrategy()

    context = {
        "opening_high": 24500,
        "current_price": 24510,
    }

    signal = strategy.generate_signal(
        context
    )

    assert signal == "BUY"



def test_nifty_orb_sell_signal():

    strategy = NiftyORBStrategy()

    context = {
        "opening_low": 24500,
        "current_price": 24490,
    }

    signal = strategy.generate_signal(
        context
    )

    assert signal == "SELL"



def test_nifty_orb_wait_signal():

    strategy = NiftyORBStrategy()

    context = {
        "opening_high": 24500,
        "opening_low": 24400,
        "current_price": 24450,
    }

    signal = strategy.generate_signal(
        context
    )

    assert signal == "WAIT"

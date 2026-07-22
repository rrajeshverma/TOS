from risk.margin_checker import MarginChecker


def test_margin_available():
    checker = MarginChecker(available_margin=50000)

    assert checker.has_sufficient_margin(10000) is True


def test_margin_insufficient():
    checker = MarginChecker(available_margin=5000)

    assert checker.has_sufficient_margin(10000) is False

from risk.exposure import Exposure


def test_exposure_within_limit():
    exposure = Exposure(max_exposure=500000)

    assert exposure.within_limit(250000) is True


def test_exposure_exceeded():
    exposure = Exposure(max_exposure=500000)

    assert exposure.within_limit(600000) is False
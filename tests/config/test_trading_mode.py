from config.trading_mode import (
    get_trading_mode,
)

from trading.execution_mode import (
    ExecutionMode,
)



def test_default_mode_is_paper(
    monkeypatch,
):

    monkeypatch.delenv(
        "TOS_MODE",
        raising=False,
    )


    mode = get_trading_mode()


    assert (
        mode
        == ExecutionMode.PAPER
    )



def test_environment_can_set_live_mode(
    monkeypatch,
):

    monkeypatch.setenv(
        "TOS_MODE",
        "LIVE",
    )


    mode = get_trading_mode()


    assert (
        mode
        == ExecutionMode.LIVE
    )



def test_environment_can_set_paper_mode(
    monkeypatch,
):

    monkeypatch.setenv(
        "TOS_MODE",
        "PAPER",
    )


    mode = get_trading_mode()


    assert (
        mode
        == ExecutionMode.PAPER
    )



def test_lowercase_live_is_supported(
    monkeypatch,
):

    monkeypatch.setenv(
        "TOS_MODE",
        "live",
    )


    mode = get_trading_mode()


    assert (
        mode
        == ExecutionMode.LIVE
    )



def test_invalid_mode_defaults_to_paper(
    monkeypatch,
):

    monkeypatch.setenv(
        "TOS_MODE",
        "INVALID",
    )


    mode = get_trading_mode()


    assert (
        mode
        == ExecutionMode.PAPER
    )

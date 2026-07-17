from optimizer.optimization_result import OptimizationResult


def test_default_result():
    result = OptimizationResult(parameters={})

    assert result.parameters == {}
    assert result.trades == 0
    assert result.wins == 0
    assert result.losses == 0
    assert result.net_profit == 0.0

def test_win_rate():
    result = OptimizationResult(
        parameters={},
        trades=100,
        wins=63,
        losses=37,
    )

    assert result.win_rate == 63.0

def test_zero_trade_win_rate():
    result = OptimizationResult(parameters={})

    assert result.win_rate == 0.0

def test_profitable():
    result = OptimizationResult(
        parameters={},
        net_profit=1000,
    )

    assert result.is_profitable

def test_not_profitable():
    result = OptimizationResult(
        parameters={},
        net_profit=-100,
    )

    assert not result.is_profitable

def test_to_dict():
    result = OptimizationResult(
        parameters={"ema": 33},
        trades=10,
    )

    data = result.to_dict()

    assert data["parameters"] == {"ema": 33}
    assert data["trades"] == 10

def test_from_dict():
    data = {
        "parameters": {"ema": 33},
        "trades": 20,
        "wins": 12,
        "losses": 8,
    }

    result = OptimizationResult.from_dict(data)

    assert result.parameters == {"ema": 33}
    assert result.trades == 20

def test_equality():
    a = OptimizationResult(parameters={"ema": 20})
    b = OptimizationResult(parameters={"ema": 20})

    assert a == b

def test_score():
    result = OptimizationResult(
        parameters={},
        net_profit=1000,
        profit_factor=2,
        sharpe_ratio=1.5,
    )

    assert result.score > 0

def test_repr():
    result = OptimizationResult(parameters={"ema": 20})

    assert "OptimizationResult" in repr(result)
from backtesting.window_generator import WindowGenerator


def test_create_generator():
    generator = WindowGenerator(
        training_size=100,
        testing_size=20,
    )

    assert generator.training_size == 100
    assert generator.testing_size == 20


def test_empty_data():
    generator = WindowGenerator(100, 20)

    assert generator.generate([]) == []


def test_not_enough_data():
    generator = WindowGenerator(100, 20)

    candles = list(range(50))

    assert generator.generate(candles) == []


def test_single_window():
    generator = WindowGenerator(100, 20)

    candles = list(range(120))

    windows = generator.generate(candles)

    assert len(windows) == 1


def test_multiple_windows():
    generator = WindowGenerator(100, 20)

    candles = list(range(300))

    windows = generator.generate(candles)

    assert len(windows) > 1


def test_window_sizes():
    generator = WindowGenerator(100, 20)

    train, test = generator.generate(
        list(range(120))
    )[0]

    assert len(train) == 100
    assert len(test) == 20


def test_windows_roll_forward():
    generator = WindowGenerator(4, 2)

    candles = list(range(10))

    windows = generator.generate(candles)

    assert windows[0] == (
        [0, 1, 2, 3],
        [4, 5],
    )

    assert windows[1] == (
        [2, 3, 4, 5],
        [6, 7],
    )
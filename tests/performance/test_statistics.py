from performance.statistics import Statistics


def test_initializes_empty():
    s = Statistics()
    assert s.count == 0


def test_add_single_value():
    s = Statistics()
    s.add(10)
    assert s.count == 1


def test_average():
    s = Statistics()
    s.add(10)
    s.add(20)
    s.add(30)
    assert s.average == 20


def test_median_odd():
    s = Statistics()
    s.add(1)
    s.add(3)
    s.add(2)
    assert s.median == 2


def test_median_even():
    s = Statistics()
    s.add(1)
    s.add(2)
    s.add(3)
    s.add(4)
    assert s.median == 2.5


def test_minimum():
    s = Statistics()
    s.add(5)
    s.add(2)
    s.add(9)
    assert s.minimum == 2


def test_maximum():
    s = Statistics()
    s.add(5)
    s.add(2)
    s.add(9)
    assert s.maximum == 9


def test_total():
    s = Statistics()
    s.add(5)
    s.add(10)
    assert s.total == 15


def test_clear():
    s = Statistics()
    s.add(1)
    s.clear()
    assert s.count == 0


def test_values():
    s = Statistics()
    s.add(1)
    s.add(2)
    assert s.values() == [1.0, 2.0]


def test_len():
    s = Statistics()
    s.add(1)
    s.add(2)
    assert len(s) == 2


def test_empty_average():
    s = Statistics()
    assert s.average == 0.0


def test_empty_median():
    s = Statistics()
    assert s.median == 0.0


def test_empty_minimum():
    s = Statistics()
    assert s.minimum == 0.0


def test_empty_maximum():
    s = Statistics()
    assert s.maximum == 0.0


def test_empty_total():
    s = Statistics()
    assert s.total == 0


def test_repr():
    s = Statistics()
    s.add(10)
    text = repr(s)
    assert "Statistics" in text


def test_multiple_clear():
    s = Statistics()
    s.add(1)
    s.clear()
    s.clear()
    assert s.count == 0


def test_reusable_after_clear():
    s = Statistics()
    s.add(1)
    s.clear()
    s.add(5)
    assert s.average == 5

from datetime import time

from strategies.filters.time_filter import TimeFilter


def test_time_before_window():
    filt = TimeFilter(
        time(10, 15),
        time(14, 30),
    )

    assert not filt.allow(
        time(10, 14),
    )


def test_time_at_start():
    filt = TimeFilter(
        time(10, 15),
        time(14, 30),
    )

    assert filt.allow(
        time(10, 15),
    )


def test_time_inside_window():
    filt = TimeFilter(
        time(10, 15),
        time(14, 30),
    )

    assert filt.allow(
        time(12, 0),
    )


def test_time_at_end():
    filt = TimeFilter(
        time(10, 15),
        time(14, 30),
    )

    assert filt.allow(
        time(14, 30),
    )


def test_time_after_window():
    filt = TimeFilter(
        time(10, 15),
        time(14, 30),
    )

    assert not filt.allow(
        time(14, 31),
    )

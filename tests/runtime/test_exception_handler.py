from runtime.exception_handler import ExceptionHandler


def test_exception_handler_records_exception():
    handler = ExceptionHandler()
    handler.record(ValueError("error"))
    assert handler.count == 1


def test_exception_handler_returns_last_exception():
    handler = ExceptionHandler()
    ex = RuntimeError("failure")
    handler.record(ex)
    assert handler.last_exception() is ex


def test_exception_handler_clear():
    handler = ExceptionHandler()
    handler.record(Exception("x"))
    handler.clear()
    assert handler.count == 0


def test_exception_handler_no_exception():
    handler = ExceptionHandler()
    assert handler.last_exception() is None


def test_exception_handler_count():
    handler = ExceptionHandler()
    handler.record(Exception("1"))
    handler.record(Exception("2"))
    assert handler.count == 2

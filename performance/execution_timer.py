import time


class ExecutionTimer:
    def __init__(self):
        self.is_running = False
        self.start_time = None
        self.end_time = None

    def start(self):
        self.is_running = True
        self.start_time = time.perf_counter()
        self.end_time = None

    def stop(self):
        self.end_time = time.perf_counter()
        self.is_running = False

    @property
    def elapsed(self):
        if self.start_time is None:
            return 0.0

        if self.end_time is None:
            return time.perf_counter() - self.start_time

        return self.end_time - self.start_time

        if self.start_time is None:
            return 0.0

        if self.end_time is None:
            return time.perf_counter() - self.start_time

        return self.end_time - self.start_time

    def start(self):
        self.is_running = True
        self.start_time = time.perf_counter()
        self.end_time = None

    def stop(self):
        if not self.is_running:
            return

        self.end_time = time.perf_counter()
        self.is_running = False

        if not self.is_running:
            return

    def __str__(self):
        return f"ExecutionTimer(elapsed={self.elapsed:.6f}s)"

    def __repr__(self):
        return str(self)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False

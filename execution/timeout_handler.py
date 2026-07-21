import time


class TimeoutHandler:

    def __init__(self, timeout_seconds):
        self.timeout_seconds = timeout_seconds

    def is_timed_out(self, start_time):
        return (time.time() - start_time) >= self.timeout_seconds

    def remaining_time(self, start_time):
        remaining = self.timeout_seconds - (time.time() - start_time)
        return max(0, remaining)
class RetryPolicy:

    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def execute(self, func):
        last_exception = None

        for _ in range(self.max_retries):
            try:
                return func()
            except Exception as exc:
                last_exception = exc

        raise last_exception
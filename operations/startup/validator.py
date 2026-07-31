from operations.startup.validation_result import ValidationResult


class StartupValidator:
    def __init__(self):
        self._checks = []

    @property
    def checks(self):
        # Keep backward compatibility with existing tests
        return self._checks

    def register(self, check):
        self._checks.append(check)
        # Preserve original API
        return None

    def run(self):
        result = ValidationResult()

        for check in self._checks:
            try:
                # Backward compatibility: callable checks
                if callable(check):
                    ok = check()
                # New API: validator objects
                elif hasattr(check, "validate"):
                    ok = check.validate()
                else:
                    raise TypeError(f"Unsupported check type: {type(check).__name__}")

                if ok is False:
                    result.success = False

            except Exception as exc:
                result.success = False
                result.message = str(exc)

        return result

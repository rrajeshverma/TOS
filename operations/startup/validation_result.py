from dataclasses import dataclass


@dataclass(slots=True)
class ValidationResult:
    success: bool = True
    message: str = ""
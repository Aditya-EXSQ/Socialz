from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False)
class DomainError(Exception):
    """
    Base class for domain/application errors.
    These are not HTTP errors; they get mapped at the edge.
    """

    code: str
    message: str
    details: Optional[dict] = None

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.code}: {self.message}"


class ConflictError(DomainError):
    def __init__(self, message: str, *, details: Optional[dict] = None) -> None:
        super().__init__(code="conflict", message=message, details=details)


class ValidationError(DomainError):
    def __init__(self, message: str, *, details: Optional[dict] = None) -> None:
        super().__init__(code="validation_error", message=message, details=details)


class NotFoundError(DomainError):
    def __init__(self, message: str, *, details: Optional[dict] = None) -> None:
        super().__init__(code="not_found", message=message, details=details)


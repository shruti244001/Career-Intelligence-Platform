"""Internal validation helpers for immutable domain models."""

import re
from datetime import datetime
from decimal import Decimal

_IDENTIFIER_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$")


def non_empty(value: str) -> str:
    """Return a trimmed non-empty string."""
    normalized = value.strip()
    if not normalized:
        raise ValueError("value must not be empty")
    return normalized


def stable_identifier(value: str) -> str:
    """Validate a stable, slug-like domain identifier."""
    normalized = non_empty(value)
    if not _IDENTIFIER_PATTERN.fullmatch(normalized):
        raise ValueError("identifier must be a lowercase slug")
    return normalized


def aware_datetime(value: datetime) -> datetime:
    """Require a datetime with a UTC offset."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value


def decimal_sum(values: list[Decimal] | tuple[Decimal, ...]) -> Decimal:
    """Sum decimal values without introducing float arithmetic."""
    return sum(values, Decimal("0"))

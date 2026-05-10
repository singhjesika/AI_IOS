"""General helper utilities."""
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def truncate(text: str, max_len: int = 200) -> str:
    return text if len(text) <= max_len else text[:max_len] + "..."


def safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
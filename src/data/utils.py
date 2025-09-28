# src/compytroller/utils.py
from datetime import datetime, date
from typing import Optional

def parse_date(x: Optional[str]) -> Optional[date]:
    """Parse various date string formats into a datetime.date.

    Supports:
    - YYYY-MM-DD
    - YYYY-MM-DDTHH:MM:SS.sss
    Returns None if parsing fails or input is falsy.
    """
    if not x:
        return None

    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(x, fmt).date()
        except (ValueError, TypeError):
            continue

    return None


def parse_float(x: Optional[str]) -> Optional[float]:
    """Convert a string to float, return None if invalid."""
    try:
        return float(x)
    except (ValueError, TypeError):
        return None


def parse_int(x: Optional[str]) -> Optional[int]:
    """Convert a string to int, return None if invalid."""
    try:
        return int(x)
    except (ValueError, TypeError):
        return None

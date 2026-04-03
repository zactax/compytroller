# src/compytroller/utils.py
import math
from datetime import date, datetime
from typing import Optional

import pandas as pd

def parse_date(x: Optional[str]) -> Optional[date]:
    """Parse various date string formats into a datetime.date.

    Supports:
    - YYYY-MM-DD
    - YYYY-MM-DDTHH:MM:SS.sss
    Returns None if parsing fails or input is falsy.
    """
    if pd.isna(x):
        return None
    elif not x:
        return None

    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(x, fmt).date()
        except (ValueError, TypeError):
            continue

    return None


def parse_float(val):
    """Convert a string to float, return None if invalid, NaN, or Inf."""
    try:
        f = float(str(val).replace(",", "")) if val not in (None, "") else None
        if f is not None and (math.isnan(f) or math.isinf(f)):
            return None
        return f
    except Exception:
        return None


def parse_int(x: Optional[str]) -> Optional[int]:
    """Convert a string to int, return None if invalid, NaN, or Inf."""
    try:
        f = float(str(x).replace(",", "")) if x not in (None, "") else None
        if f is None or math.isnan(f) or math.isinf(f):
            return None
        return int(f)
    except (ValueError, TypeError):
        return None

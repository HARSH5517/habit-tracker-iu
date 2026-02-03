"""
Date and period helper utilities.

This module provides pure helper functions to work with time periods
(daily and weekly) required for habit streak calculations.

No state is stored and no I/O is performed here.
"""

from datetime import datetime, timedelta
from typing import List


def get_period_key(dt: datetime, periodicity: str) -> str:
    """
    Compute a period key for a given datetime and periodicity.

    Daily format:
        YYYY-MM-DD

    Weekly format (ISO week):
        YYYY-WW

    Args:
        dt (datetime): The datetime to compute the period key for.
        periodicity (str): Either "daily" or "weekly".

    Returns:
        str: Period key string.

    Raises:
        ValueError: If periodicity is invalid.
    """
    if periodicity == "daily":
        return dt.strftime("%Y-%m-%d")

    if periodicity == "weekly":
        iso_year, iso_week, _ = dt.isocalendar()
        return f"{iso_year}-{iso_week:02d}"

    raise ValueError("Periodicity must be 'daily' or 'weekly'.")


def generate_period_keys(
    start: datetime,
    end: datetime,
    periodicity: str
) -> List[str]:
    """
    Generate all expected period keys between two dates (inclusive).

    This is used for streak calculation to detect missing periods.

    Args:
        start (datetime): Start datetime.
        end (datetime): End datetime.
        periodicity (str): Either "daily" or "weekly".

    Returns:
        List[str]: Ordered list of period keys.

    Raises:
        ValueError: If periodicity is invalid.
    """
    if start > end:
        start, end = end, start

    period_keys = []

    current = start

    if periodicity == "daily":
        while current.date() <= end.date():
            period_keys.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        return period_keys

    if periodicity == "weekly":
        # Normalize to the start of the ISO week (Monday)
        current = current - timedelta(days=current.weekday())

        while current <= end:
            iso_year, iso_week, _ = current.isocalendar()
            period_keys.append(f"{iso_year}-{iso_week:02d}")
            current += timedelta(weeks=1)
        return period_keys

    raise ValueError("Periodicity must be 'daily' or 'weekly'.")

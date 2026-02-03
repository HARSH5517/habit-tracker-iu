"""
Validation helper functions.

This module contains small, reusable validation utilities used mainly
by the Command Line Interface (CLI). All functions are independent,
testable, and do not perform any I/O operations.
"""

from datetime import datetime
from typing import Optional


ALLOWED_PERIODICITIES = {"daily", "weekly"}


# ------------------------------------------------------------------
# Domain validations
# ------------------------------------------------------------------

def validate_periodicity(value: str) -> str:
    """
    Validate habit periodicity.

    Args:
        value (str): User input periodicity.

    Returns:
        str: Validated periodicity.

    Raises:
        ValueError: If periodicity is invalid.
    """
    if not isinstance(value, str):
        raise ValueError("Periodicity must be a string.")

    value = value.strip().lower()

    if value not in ALLOWED_PERIODICITIES:
        raise ValueError(
            "Invalid periodicity. Allowed values: daily, weekly."
        )

    return value


def validate_habit_name(name: str) -> str:
    """
    Validate habit name is non-empty.

    Args:
        name (str): Habit name.

    Returns:
        str: Cleaned habit name.

    Raises:
        ValueError: If name is invalid.
    """
    if not isinstance(name, str):
        raise ValueError("Habit name must be a string.")

    name = name.strip()

    if not name:
        raise ValueError("Habit name cannot be empty.")

    return name


# ------------------------------------------------------------------
# CLI input validations
# ------------------------------------------------------------------

def validate_int_input(
    value: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None
) -> int:
    """
    Validate integer input from CLI menu selections.

    Args:
        value (str): Raw input value.
        min_value (int, optional): Minimum allowed value.
        max_value (int, optional): Maximum allowed value.

    Returns:
        int: Validated integer.

    Raises:
        ValueError: If value is not a valid integer or out of range.
    """
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError("Input must be an integer.")

    if min_value is not None and number < min_value:
        raise ValueError(f"Value must be >= {min_value}.")

    if max_value is not None and number > max_value:
        raise ValueError(f"Value must be <= {max_value}.")

    return number


def parse_datetime_input(
    value: str,
    format: str = "%Y-%m-%d %H:%M"
) -> datetime:
    """
    Parse user-provided datetime string.

    Default format:
        YYYY-MM-DD HH:MM

    Args:
        value (str): Raw datetime input.
        format (str): Expected datetime format.

    Returns:
        datetime: Parsed datetime object.

    Raises:
        ValueError: If parsing fails.
    """
    if not isinstance(value, str):
        raise ValueError("Datetime input must be a string.")

    try:
        return datetime.strptime(value.strip(), format)
    except ValueError:
        raise ValueError(
            f"Invalid datetime format. Expected: {format}"
        )

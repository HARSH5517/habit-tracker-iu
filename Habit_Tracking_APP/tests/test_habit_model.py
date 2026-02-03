"""
Unit tests for the Habit domain model.

These tests validate:
- Periodicity validation
- Habit check-off behavior
- JSON serialization round-trip integrity
- Allowing multiple check-offs in the same period
"""

import pytest
from datetime import datetime, timedelta

from models.habit import Habit


# ------------------------------------------------------------------
# Validation tests
# ------------------------------------------------------------------

def test_invalid_periodicity_raises_error():
    """
    Habit should reject invalid periodicity values.
    """
    with pytest.raises(ValueError):
        Habit(name="Invalid Habit", periodicity="monthly")


def test_valid_periodicities_are_accepted():
    """
    Habit should accept 'daily' and 'weekly' periodicities.
    """
    habit_daily = Habit(name="Daily Habit", periodicity="daily")
    habit_weekly = Habit(name="Weekly Habit", periodicity="weekly")

    assert habit_daily.periodicity == "daily"
    assert habit_weekly.periodicity == "weekly"


# ------------------------------------------------------------------
# Check-off behavior
# ------------------------------------------------------------------

def test_check_off_adds_completion():
    """
    check_off() should add a completion timestamp.
    """
    habit = Habit(name="Test Habit", periodicity="daily")

    habit.check_off()

    assert len(habit.completions) == 1
    assert isinstance(habit.completions[0], datetime)


def test_multiple_check_offs_in_same_period_allowed():
    """
    Multiple check-offs within the same period should be allowed.
    """
    habit = Habit(name="Multiple Checkoffs", periodicity="daily")

    now = datetime.utcnow()
    habit.check_off(now)
    habit.check_off(now + timedelta(hours=1))

    assert len(habit.completions) == 2


# ------------------------------------------------------------------
# Serialization tests
# ------------------------------------------------------------------

def test_to_dict_and_from_dict_round_trip():
    """
    Habit serialized with to_dict() and restored with from_dict()
    should preserve all data.
    """
    habit = Habit(name="Serialization Test", periodicity="daily")
    habit.check_off(datetime(2024, 1, 1, 9, 0))
    habit.check_off(datetime(2024, 1, 2, 9, 0))

    data = habit.to_dict()
    restored = Habit.from_dict(data)

    assert restored.id == habit.id
    assert restored.name == habit.name
    assert restored.periodicity == habit.periodicity
    assert restored.created_at == habit.created_at
    assert restored.completions == habit.completions

"""
Functional analytics module for habit tracking.

This module provides pure functions to analyze habit data.
No file I/O, no printing, and no state mutation are performed here.

Streak definition:
- A habit is considered completed for a period if it has at least one
  completion within that period.
- A streak is a sequence of consecutive completed periods.
- Missing any expected period breaks the streak.
"""

from typing import List, Tuple, Optional
from datetime import datetime

from models.habit import Habit
from utils.dates import get_period_key, generate_period_keys


# ------------------------------------------------------------------
# Basic listing functions
# ------------------------------------------------------------------

def list_all_habits(habits: List[Habit]) -> List[Habit]:
    """
    Return all habits.

    Args:
        habits (List[Habit]): List of habits.

    Returns:
        List[Habit]: All habits.
    """
    return list(habits)


def list_habits_by_periodicity(
    habits: List[Habit],
    periodicity: str
) -> List[Habit]:
    """
    Filter habits by periodicity.

    Args:
        habits (List[Habit]): List of habits.
        periodicity (str): "daily" or "weekly".

    Returns:
        List[Habit]: Habits matching the given periodicity.
    """
    return [h for h in habits if h.periodicity == periodicity]


# ------------------------------------------------------------------
# Streak calculations
# ------------------------------------------------------------------

def longest_streak_for_habit(habit: Habit) -> int:
    """
    Calculate the longest streak for a single habit.

    Args:
        habit (Habit): Habit to analyze.

    Returns:
        int: Length of the longest consecutive streak.
    """
    completions = habit.get_completion_timestamps()

    if not completions:
        return 0

    # Determine completed periods
    completed_periods = {
        get_period_key(dt, habit.periodicity) for dt in completions
    }

    start_date = min(completions)
    end_date = max(completions)

    expected_periods = generate_period_keys(
        start=start_date,
        end=end_date,
        periodicity=habit.periodicity
    )

    longest_streak = 0
    current_streak = 0

    for period in expected_periods:
        if period in completed_periods:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0

    return longest_streak


def longest_streak_all(
    habits: List[Habit]
) -> Optional[Tuple[str, str, int]]:
    """
    Find the habit with the longest streak across all habits.

    Args:
        habits (List[Habit]): List of habits.

    Returns:
        Tuple[str, str, int] or None:
            (habit_id, habit_name, longest_streak)
            Returns None if no habits exist.
    """
    if not habits:
        return None

    best_habit = None
    best_streak = 0

    for habit in habits:
        streak = longest_streak_for_habit(habit)
        if streak > best_streak:
            best_streak = streak
            best_habit = habit

    if best_habit is None:
        return None

    return best_habit.id, best_habit.name, best_streak

"""
Unit tests for the functional analytics module.

These tests verify:
- Listing all habits
- Filtering habits by periodicity
- Longest streak calculation for a single habit
- Longest streak calculation across all habits

All tests use deterministic fixture data to allow
exact streak value assertions.
"""

from analytics.analytics import (
    list_all_habits,
    list_habits_by_periodicity,
    longest_streak_for_habit,
    longest_streak_all,
)


# ------------------------------------------------------------------
# Listing functions
# ------------------------------------------------------------------

def test_list_all_habits_returns_all(fixture_habits):
    """
    list_all_habits() should return all habits unchanged.
    """
    result = list_all_habits(fixture_habits)

    assert len(result) == 5
    assert result == fixture_habits


def test_list_habits_by_periodicity_daily(fixture_habits):
    """
    list_habits_by_periodicity() should return only daily habits.
    """
    daily_habits = list_habits_by_periodicity(fixture_habits, "daily")

    assert len(daily_habits) == 3
    assert all(h.periodicity == "daily" for h in daily_habits)


def test_list_habits_by_periodicity_weekly(fixture_habits):
    """
    list_habits_by_periodicity() should return only weekly habits.
    """
    weekly_habits = list_habits_by_periodicity(fixture_habits, "weekly")

    assert len(weekly_habits) == 2
    assert all(h.periodicity == "weekly" for h in weekly_habits)


# ------------------------------------------------------------------
# Streak calculations (single habit)
# ------------------------------------------------------------------

def test_longest_streak_for_daily_perfect_habit(fixture_habits):
    """
    Daily habit with perfect 4-week streak should return 28.
    """
    habit = fixture_habits[0]  # Drink Water (perfect daily)
    streak = longest_streak_for_habit(habit)

    assert streak == 28


def test_longest_streak_for_daily_with_missed_days(fixture_habits):
    """
    Daily habit with missed days should return correct longest streak.
    """
    habit = fixture_habits[1]  # Morning Walk (missed days)
    streak = longest_streak_for_habit(habit)

    assert streak == 9


def test_longest_streak_for_daily_with_missed_week(fixture_habits):
    """
    Daily habit with one full missed week should return correct streak.
    """
    habit = fixture_habits[2]  # Read 20 Pages (missed week)
    streak = longest_streak_for_habit(habit)

    assert streak == 14


def test_longest_streak_for_weekly_perfect(fixture_habits):
    """
    Weekly habit with perfect 4-week streak should return 4.
    """
    habit = fixture_habits[3]  # Go to the Gym
    streak = longest_streak_for_habit(habit)

    assert streak == 4


def test_longest_streak_for_weekly_with_missed_week(fixture_habits):
    """
    Weekly habit with one missed week should return correct streak.
    """
    habit = fixture_habits[4]  # Weekly Planning
    streak = longest_streak_for_habit(habit)

    assert streak == 2


# ------------------------------------------------------------------
# Streak calculations (across all habits)
# ------------------------------------------------------------------

def test_longest_streak_all(fixture_habits):
    """
    longest_streak_all() should return the habit
    with the longest streak across all habits.
    """
    result = longest_streak_all(fixture_habits)

    assert result is not None

    habit_id, habit_name, streak = result

    assert habit_name == "Drink Water"
    assert streak == 28

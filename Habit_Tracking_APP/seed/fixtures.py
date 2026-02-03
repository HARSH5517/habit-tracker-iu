"""
Predefined habit fixtures.

This module provides deterministic fixture data for the habit tracker.
It creates exactly five predefined habits (daily and weekly) and
generates four weeks of completion data for each habit.

The fixtures are intended for:
- First-run demo data
- Unit tests (stable, repeatable results)
- Validation of streak logic

All dates are fixed to ensure deterministic behavior.
"""

from datetime import datetime, timedelta
from typing import List

from models.habit import Habit


# Fixed start date (Monday) for deterministic fixtures
FIXTURE_START_DATE = datetime(2024, 1, 1)  # 2024-01-01 is a Monday


def _generate_daily_completions(
    start: datetime,
    days: int,
    skip_days: List[int] = None
) -> List[datetime]:
    """
    Generate daily completion timestamps.

    Args:
        start (datetime): Start date.
        days (int): Number of days to generate.
        skip_days (List[int], optional): Day indices to skip (0-based).

    Returns:
        List[datetime]: Completion timestamps.
    """
    skip_days = skip_days or []
    completions = []

    for i in range(days):
        if i not in skip_days:
            completions.append(start + timedelta(days=i, hours=9))
    return completions


def _generate_weekly_completions(
    start: datetime,
    weeks: int,
    skip_weeks: List[int] = None
) -> List[datetime]:
    """
    Generate weekly completion timestamps.

    Args:
        start (datetime): Start date (assumed Monday).
        weeks (int): Number of weeks to generate.
        skip_weeks (List[int], optional): Week indices to skip (0-based).

    Returns:
        List[datetime]: Completion timestamps.
    """
    skip_weeks = skip_weeks or []
    completions = []

    for i in range(weeks):
        if i not in skip_weeks:
            completions.append(start + timedelta(weeks=i, hours=10))
    return completions


def load_fixture_habits() -> List[Habit]:
    """
    Load predefined habits with four weeks of completion data.

    Habits included:
    1. Daily – Perfect streak (no missed days)
    2. Daily – Missed a few days (broken streak)
    3. Daily – Missed an entire week
    4. Weekly – Perfect streak (4 weeks)
    5. Weekly – Missed one week

    Returns:
        List[Habit]: List of predefined Habit objects.
    """

    # 1. Daily habit – perfect 4-week streak (28 days)
    habit_1 = Habit(
        name="Drink Water",
        periodicity="daily",
        created_at=FIXTURE_START_DATE
    )
    habit_1.completions = _generate_daily_completions(
        FIXTURE_START_DATE, days=28
    )

    # 2. Daily habit – missed some days
    habit_2 = Habit(
        name="Morning Walk",
        periodicity="daily",
        created_at=FIXTURE_START_DATE
    )
    habit_2.completions = _generate_daily_completions(
        FIXTURE_START_DATE,
        days=28,
        skip_days=[3, 10, 18]
    )

    # 3. Daily habit – missed an entire week
    habit_3 = Habit(
        name="Read 20 Pages",
        periodicity="daily",
        created_at=FIXTURE_START_DATE
    )
    habit_3.completions = _generate_daily_completions(
        FIXTURE_START_DATE,
        days=28,
        skip_days=list(range(14, 21))  # skip week 3 entirely
    )

    # 4. Weekly habit – perfect streak (4 weeks)
    habit_4 = Habit(
        name="Go to the Gym",
        periodicity="weekly",
        created_at=FIXTURE_START_DATE
    )
    habit_4.completions = _generate_weekly_completions(
        FIXTURE_START_DATE,
        weeks=4
    )

    # 5. Weekly habit – missed one week
    habit_5 = Habit(
        name="Weekly Planning",
        periodicity="weekly",
        created_at=FIXTURE_START_DATE
    )
    habit_5.completions = _generate_weekly_completions(
        FIXTURE_START_DATE,
        weeks=4,
        skip_weeks=[2]
    )

    return [habit_1, habit_2, habit_3, habit_4, habit_5]

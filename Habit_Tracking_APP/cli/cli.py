"""
Command Line Interface (CLI) for the Habit Tracker application.

This module provides an interactive text-based interface that allows
users to manage habits, check off completions, and view analytics.

The CLI:
- Uses built-in input() only (no external frameworks)
- Delegates persistence to the repository
- Delegates analytics to the functional analytics module
- Contains no business or analytics logic itself
"""

from datetime import datetime
from typing import List

from models.habit import Habit
from storage.repository import HabitRepository
from analytics.analytics import (
    list_all_habits,
    list_habits_by_periodicity,
    longest_streak_all,
    longest_streak_for_habit,
)
from seed.fixtures import load_fixture_habits
from utils.validators import (
    validate_habit_name,
    validate_periodicity,
    validate_int_input,
)


# ------------------------------------------------------------------
# CLI helpers
# ------------------------------------------------------------------

def _print_habits(habits: List[Habit]) -> None:
    """
    Print a numbered list of habits.
    """
    if not habits:
        print("\nNo habits found.\n")
        return

    print("\nTracked Habits:")
    for idx, habit in enumerate(habits, start=1):
        print(
            f"{idx}. {habit.name} "
            f"(ID: {habit.id}, Periodicity: {habit.periodicity})"
        )
    print()


def _select_habit(habits: List[Habit]) -> Habit:
    """
    Prompt user to select a habit from a list.

    Returns:
        Habit: Selected habit.
    """
    _print_habits(habits)

    choice = input("Select habit number: ").strip()
    index = validate_int_input(choice, 1, len(habits)) - 1
    return habits[index]


# ------------------------------------------------------------------
# Actions
# ------------------------------------------------------------------

def create_habit(repository: HabitRepository) -> None:
    """
    Create a new habit.
    """
    try:
        name = validate_habit_name(input("Enter habit name: "))
        periodicity = validate_periodicity(
            input("Enter periodicity (daily/weekly): ")
        )

        habit = Habit(name=name, periodicity=periodicity)
        repository.add(habit)

        print("✔ Habit created successfully.\n")
    except ValueError as e:
        print(f"✖ Error: {e}\n")


def delete_habit(repository: HabitRepository) -> None:
    """
    Delete an existing habit.
    """
    habits = repository.load_all()
    if not habits:
        print("No habits to delete.\n")
        return

    try:
        habit = _select_habit(habits)
        repository.delete(habit.id)
        print("✔ Habit deleted successfully.\n")
    except ValueError as e:
        print(f"✖ Error: {e}\n")


def check_off_habit(repository: HabitRepository) -> None:
    """
    Check off a habit for the current time.
    """
    habits = repository.load_all()
    if not habits:
        print("No habits to check off.\n")
        return

    try:
        habit = _select_habit(habits)
        habit.check_off(datetime.utcnow())
        repository.update(habit)
        print("✔ Habit checked off successfully.\n")
    except ValueError as e:
        print(f"✖ Error: {e}\n")


def analytics_menu(repository: HabitRepository) -> None:
    """
    Show analytics submenu.
    """
    habits = repository.load_all()

    if not habits:
        print("No habits available for analytics.\n")
        return

    print("\nAnalytics Menu")
    print("1) List all habits")
    print("2) List habits by periodicity")
    print("3) Longest streak for a habit")
    print("4) Longest streak across all habits")
    print("5) Back to main menu")

    choice = input("Select an option: ").strip()

    try:
        option = validate_int_input(choice, 1, 5)
    except ValueError as e:
        print(f"✖ Error: {e}\n")
        return

    if option == 1:
        _print_habits(list_all_habits(habits))

    elif option == 2:
        try:
            periodicity = validate_periodicity(
                input("Enter periodicity (daily/weekly): ")
            )
            filtered = list_habits_by_periodicity(habits, periodicity)
            _print_habits(filtered)
        except ValueError as e:
            print(f"✖ Error: {e}\n")

    elif option == 3:
        try:
            habit = _select_habit(habits)
            streak = longest_streak_for_habit(habit)
            print(
                f"\nLongest streak for '{habit.name}': {streak}\n"
            )
        except ValueError as e:
            print(f"✖ Error: {e}\n")

    elif option == 4:
        result = longest_streak_all(habits)
        if result:
            habit_id, habit_name, streak = result
            print(
                f"\nLongest streak overall: "
                f"{habit_name} ({streak})\n"
            )
        else:
            print("\nNo streak data available.\n")

    elif option == 5:
        return


def load_fixtures(repository: HabitRepository) -> None:
    """
    Load predefined habits with 4 weeks of fixture data.
    """
    habits = load_fixture_habits()
    repository.save_all(habits)
    print("✔ Predefined habits loaded successfully.\n")


# ------------------------------------------------------------------
# Main CLI loop
# ------------------------------------------------------------------

def run_cli(repository: HabitRepository) -> None:
    """
    Run the main CLI loop.
    """
    while True:
        print("Habit Tracker")
        print("1) Create habit")
        print("2) Delete habit")
        print("3) List habits")
        print("4) Check off habit")
        print("5) Analytics")
        print("6) Load predefined habits")
        print("7) Exit")

        choice = input("Select an option: ").strip()

        try:
            option = validate_int_input(choice, 1, 7)
        except ValueError as e:
            print(f"✖ Error: {e}\n")
            continue

        if option == 1:
            create_habit(repository)
        elif option == 2:
            delete_habit(repository)
        elif option == 3:
            _print_habits(repository.load_all())
        elif option == 4:
            check_off_habit(repository)
        elif option == 5:
            analytics_menu(repository)
        elif option == 6:
            load_fixtures(repository)
        elif option == 7:
            print("Goodbye!")
            break

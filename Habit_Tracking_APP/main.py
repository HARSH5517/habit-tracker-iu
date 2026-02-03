"""
Main entry point for the Habit Tracker application.

Responsibilities:
1. Define the JSON data storage path
2. Initialize the repository / storage layer
3. Optionally load predefined habits (fixtures) on first run
4. Launch the Command Line Interface (CLI)

Python version: 3.7+
"""

from pathlib import Path

from storage.json_store import JsonHabitRepository
from seed.fixtures import load_fixture_habits
from cli.cli import run_cli


DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "habits.json"


def ensure_data_directory() -> None:
    """
    Ensure that the data directory exists.
    """
    DATA_DIR.mkdir(exist_ok=True)


def first_run_prompt(repository: JsonHabitRepository) -> None:
    """
    Offer to load predefined habits with 4 weeks of example data
    if no habits exist yet.
    """
    existing_habits = repository.load_all()

    if existing_habits:
        return

    print("\nNo habits found (first run detected).")
    print("Would you like to load 5 predefined habits with 4 weeks of example data?")
    print("1) Yes (recommended)")
    print("2) No (start with empty tracker)")

    choice = input("Select an option (1/2): ").strip()

    if choice == "1":
        habits = load_fixture_habits()
        repository.save_all(habits)
        print("✔ Predefined habits loaded successfully.\n")
    else:
        print("✔ Starting with an empty habit tracker.\n")


def main() -> None:
    """
    Application bootstrap function.
    """
    ensure_data_directory()

    repository = JsonHabitRepository(DATA_FILE)

    first_run_prompt(repository)

    run_cli(repository)


if __name__ == "__main__":
    main()

"""
Unit tests for the JSON-based habit repository.

These tests verify:
- Save/load round-trip persistence
- Add, get, update, and delete operations
- Robust behavior when the JSON file does not exist
"""

from datetime import datetime

from models.habit import Habit
from storage.json_store import JsonHabitRepository


# ------------------------------------------------------------------
# Load / save behavior
# ------------------------------------------------------------------

def test_load_returns_empty_list_when_file_missing(temp_json_path):
    """
    Repository should return an empty list if the JSON file does not exist.
    """
    repo = JsonHabitRepository(temp_json_path)

    habits = repo.load_all()

    assert habits == []


def test_save_and_load_round_trip(temp_json_path, fixture_habits):
    """
    Saving habits and loading them back should preserve all data.
    """
    repo = JsonHabitRepository(temp_json_path)

    repo.save_all(fixture_habits)
    loaded = repo.load_all()

    assert len(loaded) == len(fixture_habits)

    for original, restored in zip(fixture_habits, loaded):
        assert original.id == restored.id
        assert original.name == restored.name
        assert original.periodicity == restored.periodicity
        assert original.created_at == restored.created_at
        assert original.completions == restored.completions


# ------------------------------------------------------------------
# CRUD operations
# ------------------------------------------------------------------

def test_add_habit(temp_json_path):
    """
    add() should persist a new habit.
    """
    repo = JsonHabitRepository(temp_json_path)
    habit = Habit(name="Test Habit", periodicity="daily")

    repo.add(habit)
    habits = repo.load_all()

    assert len(habits) == 1
    assert habits[0].id == habit.id


def test_get_habit_by_id(temp_json_path):
    """
    get() should return the correct habit by ID.
    """
    repo = JsonHabitRepository(temp_json_path)
    habit = Habit(name="Get Habit", periodicity="weekly")

    repo.add(habit)
    fetched = repo.get(habit.id)

    assert fetched is not None
    assert fetched.id == habit.id
    assert fetched.name == habit.name


def test_update_habit(temp_json_path):
    """
    update() should persist changes to an existing habit.
    """
    repo = JsonHabitRepository(temp_json_path)
    habit = Habit(name="Update Habit", periodicity="daily")

    repo.add(habit)

    habit.check_off(datetime(2024, 1, 1, 9, 0))
    repo.update(habit)

    updated = repo.get(habit.id)

    assert updated is not None
    assert len(updated.completions) == 1


def test_delete_habit(temp_json_path):
    """
    delete() should remove a habit from storage.
    """
    repo = JsonHabitRepository(temp_json_path)
    habit = Habit(name="Delete Habit", periodicity="daily")

    repo.add(habit)
    deleted = repo.delete(habit.id)

    assert deleted is True
    assert repo.load_all() == []


def test_delete_nonexistent_habit_returns_false(temp_json_path):
    """
    delete() should return False if the habit does not exist.
    """
    repo = JsonHabitRepository(temp_json_path)

    result = repo.delete("non-existent-id")

    assert result is False

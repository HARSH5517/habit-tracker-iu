"""
Pytest configuration and shared fixtures.

This module provides reusable pytest fixtures for:
- Predefined habit data (5 habits with 4 weeks of completions)
- Temporary JSON storage paths for isolated persistence tests
"""

import pytest
from pathlib import Path

from seed.fixtures import load_fixture_habits
from storage.json_store import JsonHabitRepository


# ------------------------------------------------------------------
# Fixture: predefined habits (domain-level)
# ------------------------------------------------------------------

@pytest.fixture
def fixture_habits():
    """
    Load predefined habits with deterministic 4-week completion data.

    Returns:
        list[Habit]: List of 5 predefined Habit objects.
    """
    return load_fixture_habits()


# ------------------------------------------------------------------
# Fixture: temporary JSON storage path
# ------------------------------------------------------------------

@pytest.fixture
def temp_json_path(tmp_path: Path) -> Path:
    """
    Provide a temporary JSON file path for storage tests.

    This ensures tests do not touch real application data.

    Args:
        tmp_path (Path): Pytest-provided temporary directory.

    Returns:
        Path: Path to a temporary habits.json file.
    """
    return tmp_path / "habits.json"


# ------------------------------------------------------------------
# Fixture: JSON repository using temporary path
# ------------------------------------------------------------------

@pytest.fixture
def temp_repository(temp_json_path: Path):
    """
    Provide a JsonHabitRepository instance backed by a temporary file.

    Returns:
        JsonHabitRepository: Repository using temporary storage.
    """
    return JsonHabitRepository(temp_json_path)

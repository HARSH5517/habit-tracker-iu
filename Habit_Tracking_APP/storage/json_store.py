"""
JSON-based persistence layer for habits.

This module provides a concrete implementation of the HabitRepository
interface using a JSON file for storage. It is responsible for loading,
saving, and managing habit data between user sessions.

Storage format:
- Habits are stored as a list of dictionaries
- Datetime values are serialized using ISO 8601 strings
"""

import json
from pathlib import Path
from typing import List, Optional

from datetime import datetime

from storage.repository import HabitRepository
from models.habit import Habit


class JsonHabitRepository(HabitRepository):
    """
    JSON implementation of the HabitRepository.

    This repository persists habit data in a JSON file.
    """

    def __init__(self, file_path: Path):
        """
        Initialize the repository.

        Args:
            file_path (Path): Path to the JSON file used for storage.
        """
        self.file_path = file_path

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_file(self) -> List[dict]:
        """
        Read raw habit data from the JSON file.

        Returns:
            List[dict]: List of habit dictionaries.
        """
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # Corrupted or empty file → treat as empty storage
                return []

    def _write_file(self, data: List[dict]) -> None:
        """
        Write raw habit data to the JSON file.

        Args:
            data (List[dict]): Serializable habit data.
        """
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    # ------------------------------------------------------------------
    # Repository interface implementation
    # ------------------------------------------------------------------

    def load_all(self) -> List[Habit]:
        """
        Load all habits from storage.

        Returns:
            List[Habit]: All stored habits.
        """
        raw_data = self._read_file()
        return [Habit.from_dict(item) for item in raw_data]

    def save_all(self, habits: List[Habit]) -> None:
        """
        Persist the full list of habits to storage.

        Args:
            habits (List[Habit]): Habits to save.
        """
        data = [habit.to_dict() for habit in habits]
        self._write_file(data)

    def add(self, habit: Habit) -> None:
        """
        Add a new habit to storage.

        Args:
            habit (Habit): Habit to add.
        """
        habits = self.load_all()
        habits.append(habit)
        self.save_all(habits)

    def delete(self, habit_id: str) -> bool:
        """
        Delete a habit by its ID.

        Args:
            habit_id (str): ID of the habit to delete.

        Returns:
            bool: True if the habit was deleted, False otherwise.
        """
        habits = self.load_all()
        new_habits = [h for h in habits if h.id != habit_id]

        if len(new_habits) == len(habits):
            return False

        self.save_all(new_habits)
        return True

    def get(self, habit_id: str) -> Optional[Habit]:
        """
        Retrieve a habit by its ID.

        Args:
            habit_id (str): ID of the habit.

        Returns:
            Habit or None: The habit if found, otherwise None.
        """
        habits = self.load_all()
        for habit in habits:
            if habit.id == habit_id:
                return habit
        return None

    def update(self, habit: Habit) -> None:
        """
        Update an existing habit in storage.

        Args:
            habit (Habit): Habit with updated data.

        Raises:
            ValueError: If the habit does not exist.
        """
        habits = self.load_all()

        for index, existing in enumerate(habits):
            if existing.id == habit.id:
                habits[index] = habit
                self.save_all(habits)
                return

        raise ValueError(f"Habit with id '{habit.id}' not found.")

"""
Repository interface for habit persistence.

This module defines an abstract-style base class that specifies how
habit data must be stored and retrieved. Concrete implementations
(e.g., JSON-based storage, SQLite storage) must implement this interface.

The goal is to decouple domain logic from persistence details, enabling
clean architecture and easy future extensions.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from models.habit import Habit


class HabitRepository(ABC):
    """
    Abstract base class defining the habit repository interface.

    Responsibilities:
    - Load and persist habit data
    - Provide CRUD operations for habits
    - Hide storage details from the rest of the application

    Concrete implementations must implement all abstract methods.
    """

    @abstractmethod
    def load_all(self) -> List[Habit]:
        """
        Load all stored habits.

        Returns:
            List[Habit]: All habits currently stored.
        """
        raise NotImplementedError

    @abstractmethod
    def save_all(self, habits: List[Habit]) -> None:
        """
        Persist the full list of habits to storage.

        Args:
            habits (List[Habit]): Habits to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, habit: Habit) -> None:
        """
        Add a new habit to storage.

        Args:
            habit (Habit): Habit to add.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, habit_id: str) -> bool:
        """
        Delete a habit by its ID.

        Args:
            habit_id (str): ID of the habit to delete.

        Returns:
            bool: True if the habit was deleted, False if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, habit_id: str) -> Optional[Habit]:
        """
        Retrieve a habit by its ID.

        Args:
            habit_id (str): ID of the habit.

        Returns:
            Habit or None: The requested habit, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, habit: Habit) -> None:
        """
        Update an existing habit in storage.

        Args:
            habit (Habit): Habit with updated data.
        """
        raise NotImplementedError

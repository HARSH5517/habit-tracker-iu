"""
Habit domain model.

This module defines the core Habit class used by the habit tracker.
The Habit class represents a single habit with a defined periodicity
(daily or weekly) and a history of completion timestamps.

Analytics (e.g., longest streak) are intentionally NOT implemented here.
This class only provides helper methods and clean data access required
by the analytics module.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from uuid import uuid4


ALLOWED_PERIODICITIES = {"daily", "weekly"}


@dataclass
class Habit:
    """
    Represents a habit that can be tracked periodically.

    Attributes:
        id (str): Unique identifier for the habit (UUID string).
        name (str): Human-readable name of the habit.
        periodicity (str): Either "daily" or "weekly".
        created_at (datetime): Timestamp when the habit was created.
        completions (List[datetime]): List of completion timestamps.
    """

    name: str
    periodicity: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    completions: List[datetime] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """
        Validate habit fields after initialization.
        """
        self._validate_name()
        self._validate_periodicity()

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_name(self) -> None:
        """
        Ensure habit name is a non-empty string.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Habit name must be a non-empty string.")

    def _validate_periodicity(self) -> None:
        """
        Ensure periodicity is either 'daily' or 'weekly'.
        """
        if self.periodicity not in ALLOWED_PERIODICITIES:
            raise ValueError(
                f"Invalid periodicity '{self.periodicity}'. "
                f"Allowed values: {ALLOWED_PERIODICITIES}"
            )

    # ------------------------------------------------------------------
    # Core behavior
    # ------------------------------------------------------------------

    def check_off(self, at: datetime = None) -> None:
        """
        Mark the habit as completed at a given time.

        Args:
            at (datetime, optional): Timestamp of completion.
                                     Defaults to current UTC time.
        """
        if at is None:
            at = datetime.utcnow()

        if not isinstance(at, datetime):
            raise TypeError("Completion time must be a datetime object.")

        self.completions.append(at)

    # ------------------------------------------------------------------
    # Helper methods for analytics (no analytics logic here)
    # ------------------------------------------------------------------

    def get_completion_timestamps(self) -> List[datetime]:
        """
        Return a copy of completion timestamps.

        Returns:
            List[datetime]: Completion timestamps.
        """
        return list(self.completions)

    def has_completions(self) -> bool:
        """
        Check whether the habit has at least one completion.

        Returns:
            bool: True if at least one completion exists.
        """
        return len(self.completions) > 0

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict:
        """
        Serialize the Habit to a dictionary suitable for JSON storage.

        Returns:
            dict: Serializable representation of the habit.
        """
        return {
            "id": self.id,
            "name": self.name,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "completions": [dt.isoformat() for dt in self.completions],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Habit":
        """
        Deserialize a Habit instance from a dictionary.

        Args:
            data (dict): Dictionary representation of a habit.

        Returns:
            Habit: Reconstructed Habit object.
        """
        habit = cls(
            id=data["id"],
            name=data["name"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completions=[
                datetime.fromisoformat(ts) for ts in data.get("completions", [])
            ],
        )
        return habit

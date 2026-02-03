"""
Completion domain model.

This module defines the Completion class, which represents a single
check-off event for a habit at a specific point in time.

The Completion class is intentionally lightweight and is mainly used
for clarity, documentation, and potential future extensions.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class Completion:
    """
    Represents a single completion (check-off) of a habit.

    Attributes:
        habit_id (str): ID of the habit that was completed.
        completed_at (datetime): Timestamp when the habit was completed.
    """

    habit_id: str
    completed_at: datetime

    def to_dict(self) -> Dict:
        """
        Serialize the Completion to a dictionary suitable for JSON storage.

        Returns:
            dict: Serializable representation of the completion.
        """
        return {
            "habit_id": self.habit_id,
            "completed_at": self.completed_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Completion":
        """
        Deserialize a Completion instance from a dictionary.

        Args:
            data (dict): Dictionary representation of a completion.

        Returns:
            Completion: Reconstructed Completion object.
        """
        return cls(
            habit_id=data["habit_id"],
            completed_at=datetime.fromisoformat(data["completed_at"]),
        )

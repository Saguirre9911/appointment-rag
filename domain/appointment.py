from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Appointment:
    """
    Entity representing an appointment or event.

    Attributes:
        id: Unique identifier for the appointment (e.g., UUID4 string).
        user_id: Identifier of the user who owns the appointment (e.g., "whatsapp:+123...").
        title: Short descriptive title of the appointment.
        datetime: Date and time when the appointment occurs.
        notes: Optional additional details or context for the appointment.
    """
    id: str
    user_id: str
    title: str
    datetime: datetime
    notes: Optional[str] = field(default="")

    def __post_init__(self) -> None:
        # Validate types and required fields
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("Appointment 'id' must be a non-empty string")
        if not isinstance(self.user_id, str) or not self.user_id:
            raise ValueError("Appointment 'user_id' must be a non-empty string")
        if not isinstance(self.title, str) or not self.title:
            raise ValueError("Appointment 'title' must be a non-empty string")
        if not isinstance(self.datetime, datetime):
            raise TypeError("Appointment 'datetime' must be a datetime.datetime instance")
        if self.notes is not None and not isinstance(self.notes, str):
            raise TypeError("Appointment 'notes' must be a string or None")

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the appointment instance into a JSON-serializable dict.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "datetime": self.datetime.isoformat(),
            "notes": self.notes or ""
        }
        }

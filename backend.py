"""Dummy backend that simulates a website for testing."""

import time
from typing import Optional
from dataclasses import dataclass


@dataclass
class DataEntry:
    """Represents a data entry from the website."""

    id: int
    title: str
    date: str
    status: str
    description: str


class DummyBackend:
    """Mock backend that simulates website authentication and data fetching."""

    def __init__(self):
        self.authenticated = False
        self.username: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        """Simulate login. Accepts 'admin'/'admin' or 'user'/'password'."""
        time.sleep(0.5)  # Simulate network delay

        valid_credentials = [
            ("admin", "admin"),
            ("user", "password"),
        ]

        if (username, password) in valid_credentials:
            self.authenticated = True
            self.username = username
            return True
        return False

    def logout(self):
        """Logout the current user."""
        self.authenticated = False
        self.username = None

    def fetch_data(self) -> list[DataEntry]:
        """Fetch dummy data entries."""
        if not self.authenticated:
            raise PermissionError("Not authenticated")

        time.sleep(0.3)  # Simulate network delay

        return [
            DataEntry(
                1, "Einsatz Brand", "2024-01-15", "Ausstehend", "Kleinbrand im Keller"
            ),
            DataEntry(
                2, "Technische Hilfe", "2024-01-16", "Ausstehend", "Ölspur auf Fahrbahn"
            ),
            DataEntry(
                3, "Einsatz Rettung", "2024-01-17", "Ausstehend", "Person eingeklemmt"
            ),
            DataEntry(4, "Fehlalarm", "2024-01-18", "Ausstehend", "BMA ausgelöst"),
            DataEntry(
                5, "Einsatz Brand", "2024-01-19", "Ausstehend", "Mülltonnenbrand"
            ),
        ]

    def apply_action(self, entry_id: int) -> bool:
        """Apply action to a single entry. Returns success status."""
        if not self.authenticated:
            raise PermissionError("Not authenticated")

        time.sleep(0.2)  # Simulate processing
        return True

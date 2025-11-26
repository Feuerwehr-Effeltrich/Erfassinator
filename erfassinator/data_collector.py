"""Data collector for fetching data from backend."""

from typing import Any


class DataCollector:
    """Collects data from the backend."""

    def __init__(self, backend: Any):
        self.backend = backend

    def fetch_all(self) -> list[Any]:
        """Fetch all data entries from the backend."""
        try:
            return self.backend.fetch_data()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data: {str(e)}")

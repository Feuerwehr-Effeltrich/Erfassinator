"""Action processor for executing actions on data entries."""

from typing import Any


class ActionProcessor:
    """Processes actions on data entries."""

    def __init__(self, backend: Any):
        self.backend = backend

    def process_single(self, entry_id: int) -> tuple[bool, str]:
        """
        Process action for a single entry.

        Returns:
            (success: bool, message: str)
        """
        try:
            success = self.backend.apply_action(entry_id)
            if success:
                return True, f"Action applied to entry {entry_id}"
            else:
                return False, f"Failed to apply action to entry {entry_id}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def process_all(self, entry_ids: list[int]) -> dict[int, tuple[bool, str]]:
        """
        Process action for multiple entries.

        Returns:
            Dictionary mapping entry_id to (success, message)
        """
        results = {}
        for entry_id in entry_ids:
            results[entry_id] = self.process_single(entry_id)
        return results

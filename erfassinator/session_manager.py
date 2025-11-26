"""Session manager for handling authentication."""

from typing import Any


class SessionManager:
    """Manages authentication session."""

    def __init__(self, backend: Any):
        self.backend = backend
        self._authenticated = False

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        Attempt to login with credentials.

        Returns:
            (success: bool, message: str)
        """
        try:
            success = self.backend.login(username, password)
            if success:
                self._authenticated = True
                return True, "Login erfolgreich"
            else:
                return False, "Falsche Anmeldedaten"
        except Exception as e:
            return False, f"Login fehlgeschlagen: {str(e)}"

    def logout(self):
        """Logout the current session."""
        self.backend.logout()
        self._authenticated = False

    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self._authenticated

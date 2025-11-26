"""Login dialog for user authentication."""

import tkinter as tk
from tkinter import ttk, messagebox


class LoginDialog:
    """Modal dialog for user login."""

    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Anmeldung")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)

        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._create_widgets()

        # Focus on username field
        self.username_entry.focus()

    def _create_widgets(self):
        """Create dialog widgets."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")

        # Username
        ttk.Label(frame, text="Benutzername:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Password
        ttk.Label(frame, text="Passwort:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Anmelden", command=self._on_login).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Abbrechen", command=self._on_cancel).pack(
            side=tk.LEFT, padx=5
        )

        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self._on_login())
        self.password_entry.bind("<Return>", lambda e: self._on_login())

    def _on_login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Eingabefehler", "Bitte Benutzername und Passwort eingeben"
            )
            return

        self.result = (username, password)
        self.dialog.destroy()

    def _on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.dialog.destroy()

    def show(self) -> tuple[str, str] | None:
        """Show the dialog and return credentials or None."""
        self.dialog.wait_window()
        return self.result

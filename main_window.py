"""Main application window."""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Any

from login_dialog import LoginDialog
from session_manager import SessionManager
from data_collector import DataCollector
from action_processor import ActionProcessor


class MainWindow:
    """Main application window with data table and actions."""

    def __init__(self, root: tk.Tk, backend: Any):
        self.root = root
        self.backend = backend
        self.session_manager = SessionManager(backend)
        self.data_collector = DataCollector(backend)
        self.action_processor = ActionProcessor(backend)

        self.data_entries = []

        self.root.title("Erfassinator - FW Portal Daten Manager")
        self.root.geometry("900x600")

        self._create_widgets()
        self._show_login()

    def _create_widgets(self):
        """Create main window widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Top bar with status and buttons
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.status_label = ttk.Label(top_frame, text="Nicht angemeldet")
        self.status_label.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            top_frame, text="Daten aktualisieren", command=self._refresh_data
        ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="Abmelden", command=self._logout).pack(
            side=tk.RIGHT, padx=5
        )

        # Data table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.grid(row=0, column=1, sticky="ns")

        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.grid(row=1, column=0, sticky="ew")

        # Treeview for data display
        columns = ("ID", "Title", "Date", "Status", "Description")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Titel")
        self.tree.heading("Date", text="Datum")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Description", text="Beschreibung")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=150)
        self.tree.column("Date", width=100, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        self.tree.column("Description", width=400)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        ttk.Button(
            action_frame,
            text="Berichte erfassen (Auswahl)",
            command=self._apply_to_selected,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame, text="Berichte erfassen (Alle)", command=self._apply_to_all
        ).pack(side=tk.LEFT, padx=5)

        # Progress label
        self.progress_label = ttk.Label(action_frame, text="")
        self.progress_label.pack(side=tk.RIGHT, padx=5)

        # Progress bar (always visible to reserve space)
        progress_container = ttk.Frame(main_frame, height=25)
        progress_container.grid(row=3, column=0, sticky="ew", pady=(5, 0))
        progress_container.columnconfigure(0, weight=1)
        progress_container.grid_propagate(False)

        self.progress_bar = ttk.Progressbar(progress_container, mode="determinate")
        self.progress_bar.grid(row=0, column=0, sticky="ew")

    def _show_login(self):
        """Show login dialog."""
        dialog = LoginDialog(self.root)
        credentials = dialog.show()

        if credentials:
            username, password = credentials
            self._perform_login(username, password)
        else:
            messagebox.showinfo(
                "Abgebrochen", "Anmeldung abgebrochen. Anwendung wird beendet."
            )
            self.root.quit()

    def _perform_login(self, username: str, password: str):
        """Perform login in background thread."""
        self.status_label.config(text="Anmeldung läuft...")
        self.root.update()

        def login_thread():
            success, message = self.session_manager.login(username, password)
            self.root.after(0, lambda: self._handle_login_result(success, message))

        threading.Thread(target=login_thread, daemon=True).start()

    def _handle_login_result(self, success: bool, message: str):
        """Handle login result."""
        if success:
            self.status_label.config(text=f"Angemeldet als {self.backend.username}")
            self._refresh_data()
        else:
            messagebox.showerror("Anmeldung fehlgeschlagen", message)
            self._show_login()

    def _logout(self):
        """Logout and show login dialog again."""
        self.session_manager.logout()
        self.data_entries = []
        self.tree.delete(*self.tree.get_children())
        self.status_label.config(text="Nicht angemeldet")
        self._show_login()

    def _refresh_data(self):
        """Fetch and display data."""
        if not self.session_manager.is_authenticated:
            messagebox.showwarning("Nicht angemeldet", "Bitte zuerst anmelden")
            return

        self.status_label.config(text="Daten werden geladen...")
        self.root.update()

        def fetch_thread():
            try:
                data = self.data_collector.fetch_all()
                self.root.after(0, lambda: self._display_data(data))
            except Exception as e:
                self.root.after(0, lambda: self._handle_fetch_error(str(e)))

        threading.Thread(target=fetch_thread, daemon=True).start()

    def _display_data(self, data: list[Any]):
        """Display fetched data in the table."""
        self.data_entries = data
        self.tree.delete(*self.tree.get_children())

        for entry in data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    entry.id,
                    entry.title,
                    entry.date,
                    entry.status,
                    entry.description,
                ),
            )

        self.status_label.config(text=f"{len(data)} Einträge geladen")

    def _handle_fetch_error(self, error: str):
        """Handle data fetch error."""
        self.status_label.config(text="Fehler beim Laden der Daten")
        messagebox.showerror("Fehler", f"Daten konnten nicht geladen werden: {error}")

    def _apply_to_selected(self):
        """Apply action to selected rows."""
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Keine Auswahl", "Bitte mindestens eine Zeile auswählen"
            )
            return

        # Get entry IDs from selected rows
        entry_ids = []
        for item in selected:
            values = self.tree.item(item)["values"]
            entry_ids.append(int(values[0]))

        self._execute_actions(entry_ids)

    def _apply_to_all(self):
        """Apply action to all rows."""
        if not self.data_entries:
            messagebox.showwarning(
                "Keine Daten", "Keine Daten zum Verarbeiten vorhanden"
            )
            return

        confirm = messagebox.askyesno(
            "Bestätigen",
            f"Berichte für alle {len(self.data_entries)} Einträge erfassen?",
        )

        if confirm:
            entry_ids = [entry.id for entry in self.data_entries]
            self._execute_actions(entry_ids)

    def _execute_actions(self, entry_ids: list[int]):
        """Execute actions on given entry IDs."""
        total = len(entry_ids)

        # Reset progress bar
        self.progress_bar["maximum"] = total
        self.progress_bar["value"] = 0
        self.progress_label.config(text="")

        self.root.update()

        def progress_callback(current: int, total: int):
            """Update progress bar from background thread."""
            self.root.after(0, lambda: self._update_progress(current, total))

        def process_thread():
            results = self.action_processor.process_all(entry_ids, progress_callback)
            self.root.after(0, lambda: self._handle_action_results(results))

        threading.Thread(target=process_thread, daemon=True).start()

    def _update_progress(self, current: int, total: int):
        """Update progress bar."""
        self.progress_bar["value"] = current
        self.root.update()

    def _handle_action_results(self, results: dict[int, tuple[bool, str]]):
        """Handle action processing results."""
        success_count = sum(1 for success, _ in results.values() if success)
        total = len(results)

        # Reset progress bar to 0
        self.progress_bar["value"] = 0

        self.progress_label.config(
            text=f"Abgeschlossen: {success_count}/{total} erfolgreich"
        )

        # Update status in table
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            entry_id = int(values[0])

            if entry_id in results and results[entry_id][0]:
                # Update status to "Erfasst"
                self.tree.item(
                    item,
                    values=(values[0], values[1], values[2], "Erfasst", values[4]),
                )

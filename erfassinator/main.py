"""
Erfassinator - FW Portal Daten Manager

Haupteinstiegspunkt der Anwendung.
"""

import tkinter as tk

# from erfassinator.backend import DummyBackend
from erfassinator.backend import FWPortalBackend
from erfassinator.main_window import MainWindow


def main():
    """Haupteinstiegspunkt der Anwendung."""
    # Backend erstellen
    backend = FWPortalBackend()

    # GUI erstellen und starten
    root = tk.Tk()
    app = MainWindow(root, backend)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
Erfassinator - FW Portal Daten Manager

Haupteinstiegspunkt der Anwendung.
"""

import tkinter as tk

#from backend import DummyBackend
from backend import FWPortalBackend
from main_window import MainWindow


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

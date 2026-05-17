# ============================================================
# main.py — Application Entry Point
# ============================================================
# This is the ONLY file you need to run to start the app.
#
# WHAT IT DOES:
#   1. Creates the main Tkinter window (root)
#   2. Creates an instance of StudentPlannerApp (which builds
#      the entire GUI and loads saved data)
#   3. Starts the Tkinter event loop (mainloop) which keeps
#      the window open and responsive
#
# HOW TO RUN:
#   python main.py
#
# WHAT IS mainloop()?
#   Tkinter is event-driven.  mainloop() is an infinite loop
#   that waits for events (mouse clicks, key presses, window
#   resizes) and dispatches them to the correct handler
#   functions.  The loop runs until the user closes the window.
#
# WHAT IS if __name__ == "__main__"?
#   This condition is True only when the script is run directly
#   (e.g. "python main.py").  If this file were imported by
#   another script, __name__ would be the module name instead
#   of "__main__", and the code inside would NOT run.
#   This is a standard Python practice.
# ============================================================

import tkinter as tk
from gui.main_window import StudentPlannerApp


def main():
    """Create the Tkinter root window and launch the app."""

    # Create the root window — this is the foundation of every
    # Tkinter application.  All other widgets live inside it.
    root = tk.Tk()

    # Create the application — this builds the entire GUI,
    # loads saved tasks, and sets up event handlers.
    app = StudentPlannerApp(root)

    # Start the event loop — the window stays open until
    # the user clicks the close (X) button.
    root.mainloop()


if __name__ == "__main__":
    main()

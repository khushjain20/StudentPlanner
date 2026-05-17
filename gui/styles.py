# ============================================================
# gui/styles.py
# ============================================================
# This module configures the visual appearance (theme) for
# all ttk (themed Tkinter) widgets used in the project.
#
# WHY SEPARATE STYLES?
#   Tkinter's ttk widgets use a "Style" system similar to CSS
#   in web development.  By putting all style configuration
#   in one file, we can:
#   - Change the entire look of the app from one place
#   - Add a light/dark mode toggle in the future
#   - Keep the main window code clean and focused on layout
#
# WHAT IS ttk.Style?
#   ttk.Style() lets us customise how widgets look — colours,
#   fonts, padding, etc.  We use the "clam" theme as a base
#   because it allows the most customisation on all platforms.
# ============================================================

from tkinter import ttk
from utils.constants import COLORS, FONT_BODY, FONT_HEADING


def apply_dark_theme(root):
    """
    Apply a dark colour theme to all ttk widgets.

    Parameters:
        root (tk.Tk): The main application window.

    This function configures styles for:
    - Treeview (the task table)
    - Treeview headings
    - Progressbar
    - Combobox

    It uses the 'clam' theme as a starting point because
    the default themes on Windows/Mac don't allow much
    colour customisation.
    """
    style = ttk.Style(root)
    style.theme_use("clam")

    # ---- TREEVIEW (Task Table) ----
    # The task list is displayed using a Treeview widget.
    # We style both the rows and the column headings.

    style.configure(
        "Treeview",
        background=COLORS["card"],         # row background
        foreground=COLORS["text"],         # row text colour
        fieldbackground=COLORS["card"],    # empty area colour
        font=FONT_BODY,
        rowheight=32,                      # height of each row in pixels
    )

    style.configure(
        "Treeview.Heading",
        background=COLORS["sidebar"],      # heading background
        foreground=COLORS["accent"],       # heading text colour
        font=FONT_HEADING,
    )

    # When a row is selected, highlight it with the accent colour
    style.map(
        "Treeview",
        background=[("selected", COLORS["accent"])],
        foreground=[("selected", COLORS["bg"])],
    )

    # ---- PROGRESSBAR ----
    # The progress bar at the bottom of the window.
    # We give it a green fill on a dark trough (background).

    style.configure(
        "green.Horizontal.TProgressbar",
        troughcolor=COLORS["card"],        # background track
        background=COLORS["green"],        # filled portion
        thickness=18,                      # bar height
    )

    # ---- COMBOBOX (Priority Dropdown) ----
    # Style the dropdown to match our dark theme.

    style.configure(
        "TCombobox",
        fieldbackground=COLORS["entry_bg"],
        background=COLORS["entry_bg"],
        foreground=COLORS["text"],
    )

    # Combobox dropdown list colours
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORS["entry_bg"])],
        foreground=[("readonly", COLORS["text"])],
    )

    # ---- SCROLLBAR ----
    style.configure(
        "Vertical.TScrollbar",
        troughcolor=COLORS["card"],
        background=COLORS["entry_bg"],
    )

# ============================================================
# utils/constants.py
# ============================================================
# This file stores ALL the constant values used throughout
# the project — colours, fonts, file paths, date format, etc.
#
# WHY A SEPARATE FILE?
#   If we want to change a colour or font, we do it in ONE
#   place and it automatically applies everywhere.  This is
#   called the "Single Source of Truth" principle.
#
# NAMING CONVENTION:
#   Constants are written in UPPER_CASE with underscores,
#   which is the standard Python convention (PEP 8).
# ============================================================

import os

# -------------------- FILE PATHS --------------------

# os.path.dirname(__file__)  → folder where THIS file lives (utils/)
# We go one level up (..) to reach the project root (StudentPlanner/)
# Then into the 'data/' folder for the CSV file.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "tasks.csv")

# -------------------- CSV SETTINGS --------------------

# Column headers that appear in the first row of the CSV file
CSV_HEADERS = ["Task", "Deadline", "Priority", "Status"]

# -------------------- DATE FORMAT --------------------

# strftime/strptime format string:
#   %d = day (01-31)
#   %m = month (01-12)
#   %Y = four-digit year
DATE_FORMAT = "%d/%m/%Y"

# -------------------- PRIORITY OPTIONS --------------------

PRIORITY_OPTIONS = ["High", "Medium", "Low"]
DEFAULT_PRIORITY = "Medium"

# -------------------- STATUS VALUES --------------------

STATUS_PENDING   = "Pending"
STATUS_COMPLETED = "Completed"

# -------------------- DEADLINE THRESHOLDS --------------------

# Number of days to look ahead for "deadline is near" warnings
REMINDER_DAYS_AHEAD = 2

# -------------------- COLOUR PALETTE --------------------
# A dark-mode colour scheme inspired by the Catppuccin palette.
# Keeping all colours here makes it easy to switch themes later.

COLORS = {
    "bg":            "#1e1e2e",   # dark background
    "sidebar":       "#181825",   # slightly darker panel
    "card":          "#313244",   # card / frame background
    "accent":        "#89b4fa",   # blue accent
    "accent_hover":  "#74c7ec",   # lighter blue on hover
    "green":         "#a6e3a1",   # completed / success
    "red":           "#f38ba8",   # delete / danger
    "yellow":        "#f9e2af",   # warning / medium priority
    "orange":        "#fab387",   # high priority
    "text":          "#cdd6f4",   # primary text
    "subtext":       "#a6adc8",   # secondary text
    "placeholder":   "#6c7086",   # placeholder grey
    "entry_bg":      "#45475a",   # input field background
    "white":         "#ffffff",
}

# -------------------- FONT DEFINITIONS --------------------
# Tuples of (family, size, weight) — Tkinter's font format.

FONT_TITLE   = ("Segoe UI", 20, "bold")
FONT_HEADING = ("Segoe UI", 12, "bold")
FONT_BODY    = ("Segoe UI", 11)
FONT_SMALL   = ("Segoe UI", 10)
FONT_BUTTON  = ("Segoe UI", 10, "bold")

# -------------------- WINDOW SETTINGS --------------------

WINDOW_TITLE    = "📚 Student Planner System"
WINDOW_GEOMETRY = "960x680"
WINDOW_MIN_SIZE = (900, 640)

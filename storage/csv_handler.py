# ============================================================
# storage/csv_handler.py
# ============================================================
# This module handles ALL file operations for the project.
# It reads tasks from a CSV file and writes tasks back to it.
#
# WHY A SEPARATE FILE?
#   The GUI should NOT know how data is stored.  Tomorrow, if
#   we decide to switch from CSV to SQLite, we only need to
#   change THIS file — the rest of the project stays the same.
#   This principle is called "Separation of Concerns".
#
# HOW CSV WORKS:
#   CSV stands for Comma-Separated Values.  It is a plain text
#   file where each line is one row of data, and values within
#   a row are separated by commas.
#
#   Example:
#       Task,Deadline,Priority,Status
#       Math HW,20/05/2026,High,Pending
#       Science,25/05/2026,Medium,Completed
#
#   Python's built-in 'csv' module provides:
#   - csv.DictWriter : writes dictionaries as CSV rows
#   - csv.DictReader : reads CSV rows as dictionaries
# ============================================================

import os
import csv

from utils.constants import CSV_FILE, CSV_HEADERS, DATA_DIR


def load_tasks():
    """
    Read all tasks from the CSV file and return them as a list.

    Returns:
        list[dict]: A list of task dictionaries.
                    Each dict has keys: Task, Deadline, Priority, Status.
                    Returns an empty list if the file doesn't exist.

    How it works step-by-step:
        1. Check if the CSV file exists using os.path.exists().
        2. If it does NOT exist, return an empty list (no crash).
        3. If it exists, open it in read mode ("r").
        4. Use csv.DictReader to read each row as a dictionary.
           DictReader automatically uses the first row (headers)
           as the keys for each dictionary.
        5. Convert the reader object to a list and return it.

    Example return value:
        [
            {"Task": "Math HW", "Deadline": "20/05/2026",
             "Priority": "High", "Status": "Pending"},
            {"Task": "Science", "Deadline": "25/05/2026",
             "Priority": "Medium", "Status": "Completed"},
        ]
    """
    if not os.path.exists(CSV_FILE):
        return []

    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            tasks = [dict(row) for row in reader]
        return tasks

    except Exception as error:
        print(f"[CSV ERROR] Could not load tasks: {error}")
        return []


def save_tasks(tasks):
    """
    Write the complete task list to the CSV file.

    Parameters:
        tasks (list[dict]): The list of task dictionaries to save.

    How it works step-by-step:
        1. Ensure the data/ directory exists (create it if needed).
        2. Open the CSV file in write mode ("w").
           Write mode replaces the entire file content — this is
           simpler and safer than trying to edit individual lines.
        3. Create a csv.DictWriter with our predefined headers.
        4. Write the header row first (column names).
        5. Write all task dictionaries as rows.

    Why overwrite the whole file?
        CSV files don't support editing a single row in-place.
        The standard approach is to rewrite the entire file
        whenever data changes.  For a student planner with a
        few dozen tasks, this is fast and reliable.
    """
    # Make sure the data/ folder exists
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()       # write: Task,Deadline,Priority,Status
            writer.writerows(tasks)    # write each task dict as a row

    except Exception as error:
        print(f"[CSV ERROR] Could not save tasks: {error}")
        raise  # re-raise so the caller can show an error to the user

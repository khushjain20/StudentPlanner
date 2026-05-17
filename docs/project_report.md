# 📝 Student Planner System — Project Report

## 1. Introduction

The **Student Planner System** is a desktop application built using Python and Tkinter that helps students organise their study tasks, track deadlines, manage priorities, and monitor completion progress. The project demonstrates core programming concepts including modular design, file handling, event-driven programming, and object-oriented programming.

---

## 2. Problem Statement

Students often struggle to keep track of multiple assignments, deadlines, and priorities across different subjects. Without a proper system, tasks get missed, deadlines are forgotten, and progress is hard to measure. This project provides a simple yet effective solution in the form of a desktop planner application.

---

## 3. Objectives

1. Build a user-friendly GUI application for task management
2. Implement persistent data storage using CSV files
3. Provide deadline tracking with automatic reminders
4. Enable task search, progress tracking, and priority management
5. Follow modular programming practices with clean code structure

---

## 4. Technology Stack

| Component      | Technology           |
|----------------|----------------------|
| Language        | Python 3             |
| GUI Framework   | Tkinter + tkcalendar |
| Data Storage    | CSV (built-in `csv` module) |
| Date Handling   | `datetime` module    |
| Architecture    | Modular (multi-file) |

---

## 5. System Architecture

The project follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│              PRESENTATION LAYER             │
│         (gui/main_window.py, widgets.py)    │
│         Handles UI and user interaction     │
├─────────────────────────────────────────────┤
│              BUSINESS LOGIC LAYER           │
│  (logic/task_manager.py, reminders.py,      │
│   search.py, progress_tracker.py)           │
│  Handles rules, calculations, processing   │
├─────────────────────────────────────────────┤
│              DATA ACCESS LAYER              │
│         (storage/csv_handler.py)            │
│         Handles file read/write             │
├─────────────────────────────────────────────┤
│              DATA STORAGE                   │
│         (data/tasks.csv)                    │
│         Persistent file storage             │
└─────────────────────────────────────────────┘
```

---

## 6. Module Description

### 6.1 `main.py` — Entry Point
Creates the Tkinter root window and launches the application. Contains the `if __name__ == "__main__"` guard.

### 6.2 `gui/main_window.py` — Main GUI
Builds all UI elements (header, input fields, buttons, task table, progress bar) and handles user events by delegating to logic modules.

### 6.3 `gui/widgets.py` — Custom Widgets
Contains `PlaceholderEntry`, a custom Entry widget that shows grey placeholder text that disappears when the user clicks in.

### 6.4 `gui/styles.py` — Theme Configuration
Applies a dark colour theme to all ttk widgets (Treeview, Combobox, Progressbar, Scrollbar) using the `clam` base theme.

### 6.5 `logic/task_manager.py` — Task Operations
`TaskManager` class that manages the in-memory task list. Provides methods: `add_task()`, `delete_task()`, `mark_complete()`, `clear_all()`.

### 6.6 `logic/reminders.py` — Deadline Checker
`check_deadlines()` function that compares task deadlines against today's date and returns warning messages for overdue, due-today, and near-deadline tasks.

### 6.7 `logic/search.py` — Search Filter
`filter_tasks()` function that performs case-insensitive substring matching to filter tasks by name.

### 6.8 `logic/progress_tracker.py` — Progress Stats
`calculate_progress()` function that returns total tasks, completed tasks, and completion percentage.

### 6.9 `storage/csv_handler.py` — File I/O
`load_tasks()` and `save_tasks()` functions that read from and write to the CSV file using Python's built-in `csv` module.

### 6.10 `utils/constants.py` — Configuration
Central configuration file with all constants: colours, fonts, file paths, CSV headers, priority options, and window settings.

### 6.11 `utils/validators.py` — Input Validation
Validation functions that return `(is_valid, error_message)` tuples for clean error handling.

### 6.12 `utils/helpers.py` — Utility Functions
Date formatting and parsing helper functions used across multiple modules.

---

## 7. Key Features

| Feature              | Description                                                |
|----------------------|------------------------------------------------------------|
| Add Task             | Enter name, select deadline & priority, click Add          |
| Delete Task          | Select and remove with confirmation dialog                 |
| Mark Complete        | Change task status from Pending to Completed               |
| Clear All            | Remove all tasks with double confirmation                  |
| CSV Storage          | Auto-save on every change, auto-load on startup            |
| Calendar Picker      | Visual date selection using tkcalendar DateEntry           |
| Deadline Reminders   | Pop-up alerts for overdue, today, and near-deadline tasks  |
| Dynamic Search       | Live filtering as user types in the search bar             |
| Progress Bar         | Visual progress with percentage and task counts            |
| Placeholder Text     | Modern hint text in input fields                           |
| Dark Theme           | Professional dark colour scheme                            |

---

## 8. Data Flow Diagram

```
User Action (e.g. "Add Task")
    │
    ▼
gui/main_window.py  →  Reads input from widgets
    │
    ▼
utils/validators.py  →  Validates input (non-empty, etc.)
    │
    ▼
logic/task_manager.py  →  Creates task dict, appends to list
    │
    ▼
storage/csv_handler.py  →  Writes all tasks to data/tasks.csv
    │
    ▼
gui/main_window.py  →  Refreshes Treeview display
    │
    ▼
logic/progress_tracker.py  →  Recalculates stats
    │
    ▼
gui/main_window.py  →  Updates counter label & progress bar
```

---

## 9. OOP Concepts Demonstrated

| Concept       | Where Used                                             |
|---------------|--------------------------------------------------------|
| Class         | `TaskManager`, `StudentPlannerApp`, `PlaceholderEntry` |
| Inheritance   | `PlaceholderEntry` extends `tk.Entry`                  |
| Encapsulation | Private methods prefixed with `_` in GUI class         |
| Modularity    | Separate files for each concern                        |

---

## 10. Error Handling

- Empty task name → warning messagebox
- No task selected → warning messagebox
- CSV file missing → starts with empty list (no crash)
- CSV read/write error → error message with exception details
- Invalid date format → silently skipped during deadline check
- Delete / Clear actions → confirmation dialogs

---

## 11. Limitations

1. No edit functionality (must delete and re-add to modify)
2. CSV storage is not suitable for very large datasets
3. No multi-user support
4. No data encryption or password protection
5. Search is limited to task name only

---

## 12. Future Enhancements

1. Add task editing capability
2. Subject/category tagging
3. SQLite database for better performance
4. Dark/Light mode toggle
5. Export tasks to PDF
6. Notification sounds
7. Cloud sync with Google Sheets
8. Multiple user profiles

---

## 13. Conclusion

The Student Planner System successfully demonstrates how Python and Tkinter can be used to build a practical, well-structured desktop application. The modular architecture makes the codebase easy to understand, maintain, and extend. The project covers essential programming concepts including file handling, event-driven programming, OOP, and modular design — all of which are fundamental to software engineering.

---

*Prepared for B.Tech CSE academic submission*

# 📚 Student Planner System

**A modular desktop application for student task management built with Python & Tkinter.**

| Detail         | Value                                     |
|----------------|-------------------------------------------|
| **Language**   | Python 3                                  |
| **GUI**        | Tkinter + tkcalendar                      |
| **Storage**    | CSV (Comma-Separated Values)              |
| **Architecture** | Modular (multi-file, layered)           |
| **Level**      | Beginner-to-Intermediate                  |

---

## 📖 Project Objective

Build a desktop-based student productivity system that helps students organise study tasks, deadlines, priorities, and completion tracking in a professional, modular codebase.

---

## 🗂 Project Structure

```
StudentPlanner/
│
├── main.py                     ← Entry point — run this file
├── requirements.txt            ← External dependencies
├── README.md                   ← This file
│
├── gui/                        ← Presentation Layer (User Interface)
│   ├── __init__.py
│   ├── main_window.py          ← Main application window & event handlers
│   ├── widgets.py              ← Custom widgets (PlaceholderEntry)
│   └── styles.py               ← Dark theme configuration for ttk
│
├── logic/                      ← Business Logic Layer
│   ├── __init__.py
│   ├── task_manager.py         ← Task CRUD operations (add/delete/complete)
│   ├── reminders.py            ← Deadline checking & warning messages
│   ├── search.py               ← Task search/filter functionality
│   └── progress_tracker.py     ← Completion statistics calculator
│
├── storage/                    ← Data Access Layer
│   ├── __init__.py
│   └── csv_handler.py          ← CSV file read/write operations
│
├── utils/                      ← Shared Utilities
│   ├── __init__.py
│   ├── constants.py            ← All constants (colours, fonts, paths)
│   ├── validators.py           ← Input validation functions
│   └── helpers.py              ← Date formatting/parsing helpers
│
├── data/                       ← Data Storage
│   └── tasks.csv               ← Auto-created when you add first task
│
├── assets/                     ← Static Resources
│   ├── icons/                  ← For future icon files
│   └── screenshots/            ← For documentation screenshots
│
└── docs/                       ← Documentation
    ├── project_report.md       ← Formal project report
    └── viva_questions.md       ← Viva Q&A preparation (27 questions)
```

### Why This Structure?

| Folder     | Purpose                                      | Benefit                                    |
|------------|----------------------------------------------|--------------------------------------------|
| `gui/`     | All visual/UI code                           | Change the UI without touching logic       |
| `logic/`   | All business rules & calculations            | Reusable even without a GUI                |
| `storage/` | File I/O operations                          | Switch CSV → SQLite by changing one file   |
| `utils/`   | Shared constants, validators, helpers        | Avoid code duplication across modules      |
| `data/`    | Runtime data files                           | Keep data separate from code               |
| `assets/`  | Static resources (icons, images)             | Organised resource management              |
| `docs/`    | Project documentation                        | Easy access for submission & viva          |

---

## ⚙️ Installation & Setup

### Step 1 — Ensure Python 3 is installed

```bash
python3 --version
```

### Step 2 — Install the required library

```bash
pip install tkcalendar
```

> **Note:** `tkinter` comes pre-installed with Python. If missing:
> - **macOS:** `brew install python-tk`
> - **Ubuntu:** `sudo apt install python3-tk`
> - **Windows:** Included with official Python installer

### Step 3 — Run the application

```bash
cd StudentPlanner
python3 main.py
```

---

## ✨ Features

| #  | Feature                | Module                        |
|----|------------------------|-------------------------------|
| 1  | Add Tasks              | `logic/task_manager.py`       |
| 2  | Mark Complete          | `logic/task_manager.py`       |
| 3  | Delete Tasks           | `logic/task_manager.py`       |
| 4  | Clear All              | `logic/task_manager.py`       |
| 5  | Structured Display     | `gui/main_window.py`         |
| 6  | CSV Auto-Save          | `storage/csv_handler.py`     |
| 7  | CSV Auto-Load          | `storage/csv_handler.py`     |
| 8  | Task Counter           | `logic/progress_tracker.py`  |
| 9  | Deadline Reminders     | `logic/reminders.py`         |
| 10 | Dynamic Search         | `logic/search.py`            |
| 11 | Progress Bar           | `logic/progress_tracker.py`  |

---

## 🔄 Data Flow

```
User clicks "Add Task"
        │
        ▼
  gui/main_window.py        →  Reads input fields
        │
        ▼
  utils/validators.py       →  Validates task name
        │
        ▼
  logic/task_manager.py     →  Creates task, adds to list
        │
        ▼
  storage/csv_handler.py    →  Saves list to data/tasks.csv
        │
        ▼
  gui/main_window.py        →  Refreshes Treeview table
        │
        ▼
  logic/progress_tracker.py →  Recalculates stats
        │
        ▼
  gui/main_window.py        →  Updates counter & progress bar
```

---

## 📁 Module Explanations

### `main.py` — Entry Point
The only file you run. Creates the Tkinter root window and starts the application.

### `gui/widgets.py` — PlaceholderEntry
Custom Entry widget with grey hint text that disappears on click and reappears when empty. Uses `<FocusIn>` and `<FocusOut>` event binding.

### `gui/styles.py` — Dark Theme
Configures ttk widget appearances (Treeview, Combobox, Progressbar) using the `clam` base theme.

### `gui/main_window.py` — Main Window
Builds the entire UI, handles button clicks and key events, delegates to logic modules, and refreshes the display.

### `logic/task_manager.py` — TaskManager Class
Manages the in-memory task list with `add_task()`, `delete_task()`, `mark_complete()`, and `clear_all()`. Auto-saves to CSV after every change.

### `logic/reminders.py` — Deadline Checker
Compares task deadlines to today's date and returns warning messages (overdue, due today, due within 2 days).

### `logic/search.py` — Search Filter
Case-insensitive substring matching. Returns a filtered list without modifying the original.

### `logic/progress_tracker.py` — Progress Calculator
Returns `{"total": N, "completed": M, "percentage": P}` for display in the progress bar.

### `storage/csv_handler.py` — CSV File Handler
`load_tasks()` reads from CSV, `save_tasks()` writes to CSV. The GUI never touches files directly.

### `utils/constants.py` — Configuration Hub
All colours, fonts, paths, headers, and settings in one file. Change a colour here → it changes everywhere.

### `utils/validators.py` — Input Validators
Functions returning `(is_valid, error_message)` tuples. Clean pattern for error handling.

### `utils/helpers.py` — Date Utilities
`format_date()`, `parse_date()`, `get_today()` — shared by multiple modules.

---

## 📋 CSV File Format

```csv
Task,Deadline,Priority,Status
Math Assignment,20/05/2026,High,Pending
Science Project,25/05/2026,Medium,Completed
```

Stored at: `data/tasks.csv` (auto-created on first task).

---

## 🚀 Suggested Future Improvements

1. Edit existing tasks without delete-and-readd
2. Subject/category tagging system
3. Migrate from CSV to SQLite database
4. Dark/Light theme toggle
5. Export task report to PDF
6. Unit tests for logic modules
7. Notification sounds for reminders
8. Cloud sync with Google Sheets

---

## 📄 Documentation

- **[Project Report](docs/project_report.md)** — Formal academic report with architecture, data flow, and OOP concepts
- **[Viva Questions](docs/viva_questions.md)** — 27 Q&A covering Python, OOP, Tkinter, file handling, and architecture

---

## 📝 License

This project is created for academic and learning purposes. Feel free to use, modify, and share.

---

*Built with ❤️ using Python & Tkinter — Modular Architecture*

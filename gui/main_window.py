# ============================================================
# gui/main_window.py
# ============================================================
# This is the MAIN GUI module.  It builds the entire user
# interface and connects GUI events (button clicks, key
# presses) to the backend logic modules.
#
# ARCHITECTURE:
#   main_window.py is the "glue" between the user and the
#   backend.  It does NOT contain business logic — it only:
#   1. Builds and arranges widgets on the screen
#   2. Reads user input from widgets
#   3. Calls methods from logic/ modules
#   4. Displays results back to the user
#
# DATA FLOW:
#   User clicks "Add Task"
#       → main_window reads input fields
#       → calls task_manager.add_task(name, date, priority)
#       → task_manager saves to CSV via csv_handler
#       → main_window refreshes the Treeview display
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

# tkcalendar provides the DateEntry calendar widget
from tkcalendar import DateEntry

# --- Import our project modules ---
from gui.widgets import PlaceholderEntry
from gui.styles import apply_dark_theme
from logic.task_manager import TaskManager
from logic.reminders import check_deadlines
from logic.search import filter_tasks
from logic.progress_tracker import calculate_progress
from utils.constants import (
    COLORS, FONT_TITLE, FONT_HEADING, FONT_BODY,
    FONT_SMALL, FONT_BUTTON, PRIORITY_OPTIONS,
    DEFAULT_PRIORITY, WINDOW_TITLE, WINDOW_GEOMETRY,
    WINDOW_MIN_SIZE,
)
from utils.validators import (
    validate_task_name,
    validate_task_selection,
    validate_tasks_exist,
)
from utils.helpers import format_date


class StudentPlannerApp:
    """
    Main application class that builds and manages the GUI.

    This class:
    - Creates all the visual elements (widgets)
    - Handles user interactions (button clicks, key presses)
    - Delegates business logic to the logic/ modules
    - Updates the display whenever data changes

    Attributes:
        root         : The main Tkinter window
        task_manager : Instance of TaskManager (handles task data)
        task_entry   : PlaceholderEntry for task name input
        search_entry : PlaceholderEntry for search input
        date_entry   : DateEntry calendar widget
        priority_var : StringVar holding selected priority
        tree         : Treeview widget displaying tasks
        progress_bar : Progressbar widget
        counter_label: Label showing task statistics
    """

    def __init__(self, root):
        """
        Initialise the application.

        Steps:
        1. Configure the main window (title, size, colour)
        2. Apply the dark theme to ttk widgets
        3. Create the TaskManager (loads saved tasks)
        4. Build all GUI sections
        5. Display loaded tasks in the Treeview
        6. Check for deadline reminders (after 500ms delay)
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.minsize(*WINDOW_MIN_SIZE)
        self.root.configure(bg=COLORS["bg"])

        # Apply dark theme to all ttk widgets
        apply_dark_theme(self.root)

        # Create the TaskManager — this loads saved tasks from CSV
        self.task_manager = TaskManager()

        # ---------- BUILD ALL GUI SECTIONS ----------
        self._build_header()
        self._build_input_area()
        self._build_action_buttons()
        self._build_search_bar()
        self._build_task_list()
        self._build_progress_section()

        # ---------- DISPLAY LOADED TASKS ----------
        self.refresh_task_list()

        # ---------- CHECK DEADLINES AFTER WINDOW LOADS ----------
        # root.after(ms, func) schedules a function to run after
        # a delay.  We use 500ms so the window fully appears first.
        self.root.after(500, self._show_deadline_reminders)

    # ============================================================
    #  GUI BUILDER METHODS
    #  (Each method builds one section of the interface)
    # ============================================================

    def _build_header(self):
        """Build the title bar at the top of the window."""

        header = tk.Frame(self.root, bg=COLORS["sidebar"], pady=14)
        header.pack(fill=tk.X)

        # Application title
        tk.Label(
            header,
            text="📚  Student Planner System",
            font=FONT_TITLE,
            bg=COLORS["sidebar"],
            fg=COLORS["accent"],
        ).pack()

        # Subtitle
        tk.Label(
            header,
            text="Organise your study tasks, deadlines & priorities",
            font=FONT_SMALL,
            bg=COLORS["sidebar"],
            fg=COLORS["subtext"],
        ).pack()

    def _build_input_area(self):
        """
        Build the input section with:
        - Task name entry (with placeholder)
        - Deadline date picker (tkcalendar DateEntry)
        - Priority dropdown (ttk.Combobox)
        - Add Task button
        """

        input_frame = tk.Frame(self.root, bg=COLORS["bg"], pady=10)
        input_frame.pack(fill=tk.X, padx=20)

        # --- Task Name ---
        tk.Label(
            input_frame, text="Task Name", font=FONT_HEADING,
            bg=COLORS["bg"], fg=COLORS["text"],
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.task_entry = PlaceholderEntry(
            input_frame,
            placeholder="Enter Task",
            font=FONT_BODY,
            bg=COLORS["entry_bg"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            width=32,
        )
        self.task_entry.grid(row=1, column=0, padx=(0, 10), ipady=6)

        # --- Deadline Date Picker ---
        # DateEntry from tkcalendar shows a clickable calendar popup.
        # state="readonly" prevents the user from typing a date manually,
        # ensuring the format is always correct.
        tk.Label(
            input_frame, text="Deadline", font=FONT_HEADING,
            bg=COLORS["bg"], fg=COLORS["text"],
        ).grid(row=0, column=1, sticky="w", padx=(0, 10))

        self.date_entry = DateEntry(
            input_frame,
            width=14,
            font=FONT_BODY,
            background=COLORS["accent"],
            foreground=COLORS["white"],
            headersbackground=COLORS["sidebar"],
            headersforeground=COLORS["text"],
            selectbackground=COLORS["accent"],
            date_pattern="dd/MM/yyyy",
            state="readonly",
        )
        self.date_entry.grid(row=1, column=1, padx=(0, 10), ipady=4)

        # --- Priority Dropdown ---
        tk.Label(
            input_frame, text="Priority", font=FONT_HEADING,
            bg=COLORS["bg"], fg=COLORS["text"],
        ).grid(row=0, column=2, sticky="w", padx=(0, 10))

        self.priority_var = tk.StringVar(value=DEFAULT_PRIORITY)
        self.priority_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=PRIORITY_OPTIONS,
            state="readonly",
            font=FONT_BODY,
            width=10,
        )
        self.priority_dropdown.grid(row=1, column=2, padx=(0, 10), ipady=4)

        # --- Add Task Button ---
        tk.Button(
            input_frame,
            text="＋  Add Task",
            font=FONT_BUTTON,
            bg=COLORS["accent"],
            fg=COLORS["bg"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["bg"],
            relief="flat",
            cursor="hand2",
            padx=16, pady=6,
            command=self._on_add_task,
        ).grid(row=1, column=3, padx=(10, 0), ipady=2)

    def _build_action_buttons(self):
        """Build the row of action buttons below the input area."""

        btn_frame = tk.Frame(self.root, bg=COLORS["bg"], pady=6)
        btn_frame.pack(fill=tk.X, padx=20)

        # Each tuple: (button_text, button_colour, handler_function)
        buttons = [
            ("✓  Mark Complete",    COLORS["green"],  self._on_mark_complete),
            ("✕  Delete Task",      COLORS["red"],    self._on_delete_task),
            ("⟳  Clear All",        COLORS["yellow"], self._on_clear_all),
            ("⚠  Check Deadlines",  COLORS["orange"], self._show_deadline_reminders),
        ]

        for idx, (text, color, command) in enumerate(buttons):
            tk.Button(
                btn_frame,
                text=text,
                font=FONT_BUTTON,
                bg=color,
                fg=COLORS["bg"],
                activebackground=color,
                relief="flat",
                cursor="hand2",
                padx=14, pady=5,
                command=command,
            ).grid(row=0, column=idx, padx=5)

    def _build_search_bar(self):
        """Build the search bar with a magnifying glass icon."""

        search_frame = tk.Frame(self.root, bg=COLORS["bg"], pady=6)
        search_frame.pack(fill=tk.X, padx=20)

        # Search icon
        tk.Label(
            search_frame, text="🔍", font=FONT_BODY,
            bg=COLORS["bg"], fg=COLORS["subtext"],
        ).pack(side=tk.LEFT, padx=(0, 6))

        # Search entry with placeholder
        self.search_entry = PlaceholderEntry(
            search_frame,
            placeholder="Search tasks...",
            font=FONT_BODY,
            bg=COLORS["entry_bg"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            width=40,
        )
        self.search_entry.pack(side=tk.LEFT, ipady=5, fill=tk.X, expand=True)

        # Bind <KeyRelease> so search updates live as user types
        self.search_entry.bind("<KeyRelease>", self._on_search)

    def _build_task_list(self):
        """
        Build the Treeview table that displays all tasks.

        Treeview is a tkinter widget that shows data in rows
        and columns — similar to a spreadsheet.
        """

        list_frame = tk.Frame(self.root, bg=COLORS["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(4, 8))

        # Define column identifiers
        columns = ("task", "deadline", "priority", "status")

        # Create the Treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",       # hide the default tree column
            selectmode="browse",   # allow single-row selection only
        )

        # Configure column headings and widths
        self.tree.heading("task",     text="Task Name")
        self.tree.heading("deadline", text="Deadline")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status",   text="Status")

        self.tree.column("task",     width=320, anchor="w")
        self.tree.column("deadline", width=130, anchor="center")
        self.tree.column("priority", width=110, anchor="center")
        self.tree.column("status",   width=110, anchor="center")

        # Scrollbar (for when there are many tasks)
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_progress_section(self):
        """Build the bottom bar with task counter and progress bar."""

        progress_frame = tk.Frame(self.root, bg=COLORS["sidebar"], pady=10)
        progress_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Task counter label
        self.counter_label = tk.Label(
            progress_frame,
            text="Total: 0  |  Completed: 0  |  Progress: 0%",
            font=FONT_BODY,
            bg=COLORS["sidebar"],
            fg=COLORS["text"],
        )
        self.counter_label.pack(side=tk.LEFT, padx=20)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            length=260,
            mode="determinate",
            style="green.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=20)

    # ============================================================
    #  EVENT HANDLER METHODS
    #  (Called when the user clicks buttons or types)
    # ============================================================

    def _on_add_task(self):
        """
        Handle the "Add Task" button click.

        Flow:
        1. Read input from task entry, date picker, priority
        2. Validate the task name
        3. Call task_manager.add_task()
        4. Clear the input field
        5. Refresh the display
        """
        task_name = self.task_entry.get_value()

        # Validate
        is_valid, error_msg = validate_task_name(task_name)
        if not is_valid:
            messagebox.showwarning("Empty Task", error_msg)
            return

        # Read deadline and priority
        deadline_date = self.date_entry.get_date()
        deadline_str = format_date(deadline_date)
        priority = self.priority_var.get()

        # Add task via TaskManager
        self.task_manager.add_task(task_name, deadline_str, priority)

        # Clear input and refresh display
        self.task_entry.clear_field()
        self.task_entry.master.focus()   # remove focus from entry
        self.refresh_task_list()

        messagebox.showinfo("Success", f"Task '{task_name}' added! ✓")

    def _on_delete_task(self):
        """
        Handle the "Delete Task" button click.

        Flow:
        1. Check if a task is selected in the Treeview
        2. Ask for confirmation
        3. Call task_manager.delete_task()
        4. Refresh the display
        """
        selected = self.tree.selection()

        is_valid, error_msg = validate_task_selection(selected)
        if not is_valid:
            messagebox.showwarning("No Selection", error_msg)
            return

        # Get the task name from the selected row
        item = self.tree.item(selected[0])
        task_name = item["values"][0]

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\"{task_name}\"?"
        )

        if confirm:
            self.task_manager.delete_task(task_name)
            self.refresh_task_list()

    def _on_mark_complete(self):
        """
        Handle the "Mark Complete" button click.

        Flow:
        1. Check if a task is selected
        2. Call task_manager.mark_complete()
        3. Show appropriate message based on result
        4. Refresh the display
        """
        selected = self.tree.selection()

        is_valid, error_msg = validate_task_selection(selected)
        if not is_valid:
            messagebox.showwarning("No Selection", error_msg)
            return

        task_name = self.tree.item(selected[0])["values"][0]

        # mark_complete returns: "completed", "already", or "not_found"
        result = self.task_manager.mark_complete(task_name)

        if result == "completed":
            self.refresh_task_list()
            messagebox.showinfo("Completed", f"'{task_name}' marked as done! ✓")
        elif result == "already":
            messagebox.showinfo("Already Done",
                                f"'{task_name}' is already completed!")

    def _on_clear_all(self):
        """
        Handle the "Clear All" button click.

        Flow:
        1. Check if there are any tasks
        2. Ask for confirmation
        3. Call task_manager.clear_all()
        4. Refresh the display
        """
        tasks = self.task_manager.get_all_tasks()

        is_valid, error_msg = validate_tasks_exist(tasks)
        if not is_valid:
            messagebox.showinfo("Nothing to Clear", error_msg)
            return

        confirm = messagebox.askyesno(
            "Clear All Tasks",
            "Are you sure you want to delete ALL tasks?\n"
            "This action cannot be undone."
        )

        if confirm:
            self.task_manager.clear_all()
            self.refresh_task_list()

    def _on_search(self, event=None):
        """
        Handle search bar key releases (dynamic/live search).

        Every keypress triggers this method.  We read the query,
        filter the task list, and refresh the Treeview with only
        the matching tasks.
        """
        query = self.search_entry.get_value()
        all_tasks = self.task_manager.get_all_tasks()

        if not query:
            # Empty search → show all tasks
            self.refresh_task_list()
        else:
            # Filter and display matching tasks only
            filtered = filter_tasks(all_tasks, query)
            self.refresh_task_list(display_tasks=filtered)

    def _show_deadline_reminders(self):
        """
        Check deadlines and show a pop-up with warnings.

        This is called:
        1. Automatically 500ms after the app starts
        2. Manually when the user clicks "Check Deadlines"
        """
        tasks = self.task_manager.get_all_tasks()
        reminders = check_deadlines(tasks)

        if reminders:
            messagebox.showwarning(
                "⏰ Deadline Reminders",
                "\n\n".join(reminders)
            )
        else:
            messagebox.showinfo(
                "All Clear ✓",
                "No upcoming deadlines within the next 2 days."
            )

    # ============================================================
    #  DISPLAY METHODS
    # ============================================================

    def refresh_task_list(self, display_tasks=None):
        """
        Refresh the Treeview to show current tasks.

        Parameters:
            display_tasks (list or None):
                If provided, show only these tasks (used by search).
                If None, show ALL tasks from TaskManager.

        Also updates the progress bar and counter.
        """
        # Clear all existing rows from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Decide which tasks to display
        tasks_to_show = display_tasks if display_tasks is not None \
                        else self.task_manager.get_all_tasks()

        # Insert each task as a row in the Treeview
        for task in tasks_to_show:
            # Tag rows by status for colour coding
            tag = "completed" if task["Status"] == "Completed" else "pending"

            self.tree.insert(
                "",          # parent (empty = top level)
                tk.END,      # position (append at the end)
                values=(
                    task["Task"],
                    task["Deadline"],
                    task["Priority"],
                    task["Status"],
                ),
                tags=(tag,),
            )

        # Apply colour to tags
        self.tree.tag_configure("completed", foreground=COLORS["green"])
        self.tree.tag_configure("pending",   foreground=COLORS["text"])

        # Update the progress bar and counter label
        self._update_progress()

    def _update_progress(self):
        """
        Calculate and display task completion statistics.

        Uses the progress_tracker module to get stats, then
        updates the counter label and progress bar.
        """
        all_tasks = self.task_manager.get_all_tasks()
        stats = calculate_progress(all_tasks)

        # Update the label text
        self.counter_label.config(
            text=(
                f"Total: {stats['total']}  |  "
                f"Completed: {stats['completed']}  |  "
                f"Progress: {stats['percentage']}%"
            )
        )

        # Update the progress bar (max value is 100)
        self.progress_bar["value"] = stats["percentage"]

# 🎓 Viva Questions & Answers — Student Planner System

A comprehensive list of questions a professor might ask during viva, along with clear answers.

---

## General / Conceptual Questions

### Q1: What is the objective of your project?
**A:** The objective is to build a desktop application that helps students manage study tasks, track deadlines, set priorities, and monitor their completion progress using a clean graphical interface.

### Q2: Why did you choose Python and Tkinter?
**A:** Python is easy to learn and widely used in academic projects. Tkinter comes built-in with Python so no complex setup is needed. Together, they allow us to build a GUI application quickly.

### Q3: Why did you use CSV instead of a database like SQLite?
**A:** CSV is simpler to understand and implement for a beginner project. It doesn't require installing any additional libraries or setting up a database server. For a small-scale planner with limited tasks, CSV is perfectly sufficient.

### Q4: What is the advantage of modular structure over a single file?
**A:** Modular structure:
- Makes code easier to read and maintain
- Allows team members to work on different modules independently
- Makes it easy to find and fix bugs
- Follows industry-standard software engineering practices
- Makes the project scalable for future features

---

## Python / OOP Questions

### Q5: What is `if __name__ == "__main__"`?
**A:** When Python runs a script directly, it sets the `__name__` variable to `"__main__"`. This condition ensures that `main()` only runs when we execute `main.py` directly, not when it's imported by another file.

### Q6: What is inheritance? Where did you use it?
**A:** Inheritance means creating a new class based on an existing class. `PlaceholderEntry` inherits from `tk.Entry` — it gets all the features of a normal Entry widget and adds placeholder text behaviour on top.

### Q7: What is encapsulation? Where did you use it?
**A:** Encapsulation means hiding internal details and exposing only what's necessary. In our project, methods prefixed with `_` (like `_build_header`, `_on_add_task`) are private — they are only meant to be called within the class, not from outside.

### Q8: What does `self` mean in Python classes?
**A:** `self` refers to the current instance of the class. When we write `self.tasks`, it means "the tasks list belonging to THIS specific object". Every instance method receives `self` as its first parameter.

### Q9: What is a list comprehension? Where did you use it?
**A:** A list comprehension is a concise way to create a new list by filtering or transforming an existing one. We used it in `search.py`:
```python
filtered = [task for task in tasks if query in task["Task"].lower()]
```
This creates a new list containing only tasks whose name matches the search query.

---

## Feature-Specific Questions

### Q10: How does the placeholder text work?
**A:** We bind two events to the Entry widget:
- `<FocusIn>`: When the user clicks in, if the text is the placeholder, we clear it and change colour to white.
- `<FocusOut>`: When the user clicks away, if the field is empty, we restore the placeholder in grey.

### Q11: How does the calendar date picker work?
**A:** We use `DateEntry` from the `tkcalendar` library. It shows a small dropdown calendar when clicked. The `date_pattern="dd/MM/yyyy"` parameter ensures dates display in DD/MM/YYYY format. Setting `state="readonly"` prevents manual typing.

### Q12: How does deadline checking work?
**A:** We get today's date with `datetime.now().date()`. For each pending task, we parse its deadline string into a date object using `strptime()`. Then we subtract: `days_left = (deadline - today).days`. If negative, it's overdue. If zero, it's due today. If 1-2, it's near.

### Q13: How does the search feature work in real-time?
**A:** We bind the `<KeyRelease>` event to the search entry. Every time the user types or deletes a character, our `_on_search()` method is called. It reads the query, filters the task list using case-insensitive substring matching, and refreshes the Treeview.

### Q14: How does progress tracking work?
**A:** We count total tasks and completed tasks, then calculate:
```
percentage = (completed / total) × 100
```
This value updates the counter label and the `ttk.Progressbar` widget.

---

## File Handling Questions

### Q15: How does CSV saving work?
**A:** We open the file in write mode (`"w"`) which replaces all content. Using `csv.DictWriter`, we first write the header row (column names), then write each task dictionary as a row. This function is called every time tasks change.

### Q16: How does CSV loading work?
**A:** We check if the file exists using `os.path.exists()`. If yes, we open it and use `csv.DictReader` which reads each row as a dictionary (e.g., `{"Task": "Math HW", "Deadline": "20/05/2026", ...}`). Each dictionary is appended to the task list.

### Q17: Why do you overwrite the entire CSV file each time?
**A:** CSV files don't support editing individual rows. The simplest and safest approach is to rewrite the entire file whenever data changes. For a student planner with a reasonable number of tasks, this has no performance impact.

### Q18: What happens if the CSV file doesn't exist?
**A:** `load_tasks()` checks with `os.path.exists()` first. If the file doesn't exist, it returns an empty list — no error, no crash. The file will be created automatically when the user adds their first task.

---

## Tkinter Questions

### Q19: What is `mainloop()`?
**A:** `mainloop()` is an infinite loop that keeps the window open and waits for user events (clicks, keypresses). When an event occurs, Tkinter calls the appropriate handler function. The loop ends when the user closes the window.

### Q20: What is `root.after(500, func)`?
**A:** `after()` schedules a function to run after a specified delay (in milliseconds). We use `root.after(500, check_deadlines)` so that deadline pop-ups appear 500ms after the window is fully drawn, not before the user can see the interface.

### Q21: What is a Treeview widget?
**A:** `ttk.Treeview` displays data in a table format with rows and columns. We use it to show the task list. Each row is a task, and the columns are: Task Name, Deadline, Priority, Status.

### Q22: What are `pack()`, `grid()`, and `place()`?
**A:** These are Tkinter's geometry managers — they control where widgets are positioned:
- `pack()`: Stacks widgets top-to-bottom or side-by-side
- `grid()`: Places widgets in a row-column grid (we use this for the input area)
- `place()`: Places widgets at exact x, y coordinates (we don't use this)

### Q23: What is a StringVar?
**A:** `tk.StringVar` is a special Tkinter variable that automatically updates the widget it's linked to. We use it with the Combobox — when the user selects a priority, the StringVar's value changes, and we can read it with `.get()`.

---

## Architecture Questions

### Q24: Explain the data flow when a user adds a task.
**A:**
1. User fills in task name, selects deadline and priority, clicks "Add Task"
2. `main_window.py` reads the input values
3. `validators.py` checks if the task name is not empty
4. `task_manager.py` creates a task dictionary and adds it to the list
5. `csv_handler.py` writes the updated list to `tasks.csv`
6. `main_window.py` refreshes the Treeview and updates the progress bar

### Q25: What is "Separation of Concerns"?
**A:** It means each module should handle only ONE responsibility:
- `csv_handler.py` only handles file I/O
- `task_manager.py` only manages task data
- `main_window.py` only handles the user interface
If we want to switch from CSV to SQLite, we only change `csv_handler.py` — nothing else needs to change.

---

## Bonus / Impressive Answers

### Q26: What would you improve if you had more time?
**A:** I would add:
1. Edit functionality for existing tasks
2. SQLite database for better data handling
3. Category tags for subjects
4. Export to PDF feature
5. Dark/Light theme toggle
6. Unit tests for the logic modules

### Q27: Is this project scalable?
**A:** Yes, thanks to the modular architecture. New features can be added as new modules without modifying existing code. For example, adding email reminders would just need a new `logic/email_notifier.py` file.

---

*Prepared for B.Tech CSE viva preparation*

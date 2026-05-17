# ============================================================
# logic/task_manager.py
# ============================================================
# This is the CORE module of the project.  It manages the
# list of tasks and provides methods to add, delete, complete,
# and clear tasks.
#
# DESIGN DECISION:
#   TaskManager is a class (not just loose functions) because
#   it needs to hold state — the list of tasks.  The GUI
#   creates ONE instance of TaskManager and calls its methods.
#
# DATA FLOW:
#   GUI  →  TaskManager  →  csv_handler  →  tasks.csv
#   (The GUI never touches CSV directly — it goes through
#    TaskManager, which goes through csv_handler.)
# ============================================================

from storage.csv_handler import load_tasks, save_tasks
from utils.constants import STATUS_PENDING, STATUS_COMPLETED


class TaskManager:
    """
    Manages the in-memory list of tasks and syncs with CSV.

    Attributes:
        tasks (list[dict]): The master list of task dictionaries.

    Each task dictionary looks like:
        {
            "Task":     "Math Assignment",
            "Deadline": "20/05/2026",
            "Priority": "High",
            "Status":   "Pending"
        }
    """

    def __init__(self):
        """
        Initialise the TaskManager.

        On creation, it immediately loads any saved tasks from
        the CSV file.  If the file doesn't exist yet, the list
        starts empty.
        """
        self.tasks = load_tasks()

    def get_all_tasks(self):
        """
        Return the complete list of tasks.

        Returns:
            list[dict]: All tasks currently in memory.
        """
        return self.tasks

    def add_task(self, task_name, deadline, priority):
        """
        Add a new task to the list and save to CSV.

        Parameters:
            task_name (str): Name of the task (e.g. "Math HW").
            deadline  (str): Deadline in DD/MM/YYYY format.
            priority  (str): "High", "Medium", or "Low".

        The new task always starts with Status = "Pending".
        """
        new_task = {
            "Task":     task_name,
            "Deadline": deadline,
            "Priority": priority,
            "Status":   STATUS_PENDING,
        }

        self.tasks.append(new_task)
        save_tasks(self.tasks)

    def delete_task(self, task_name):
        """
        Delete a task by its name.

        Parameters:
            task_name (str): The name of the task to remove.

        Returns:
            bool: True if a task was found and deleted,
                  False if no matching task was found.

        We loop through the list, find the first task with a
        matching name, remove it, and save the updated list.
        """
        for task in self.tasks:
            if task["Task"] == task_name:
                self.tasks.remove(task)
                save_tasks(self.tasks)
                return True

        return False

    def mark_complete(self, task_name):
        """
        Mark a task as completed.

        Parameters:
            task_name (str): The name of the task to complete.

        Returns:
            str: A status message —
                 "completed" if successfully marked,
                 "already"   if it was already completed,
                 "not_found" if no matching task exists.
        """
        for task in self.tasks:
            if task["Task"] == task_name:
                # Check if already completed
                if task["Status"] == STATUS_COMPLETED:
                    return "already"

                task["Status"] = STATUS_COMPLETED
                save_tasks(self.tasks)
                return "completed"

        return "not_found"

    def clear_all(self):
        """
        Remove ALL tasks from the list and save (empty file).

        Returns:
            int: The number of tasks that were cleared.
        """
        count = len(self.tasks)
        self.tasks.clear()
        save_tasks(self.tasks)
        return count

    def get_task_count(self):
        """
        Return the total number of tasks.

        Returns:
            int: Total task count.
        """
        return len(self.tasks)

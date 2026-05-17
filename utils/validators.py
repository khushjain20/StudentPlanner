# ============================================================
# utils/validators.py
# ============================================================
# This file contains validation functions that check user
# input before it is processed.
#
# WHY SEPARATE VALIDATORS?
#   Keeping validation logic in its own file means:
#   - The GUI code stays clean (no messy if-else chains)
#   - We can reuse validators across different parts of the app
#   - Easier to add new validation rules later
#
# Each function returns a tuple: (is_valid, error_message)
#   - is_valid      : True if input is acceptable, False otherwise
#   - error_message : A user-friendly message explaining the issue
#                     (empty string if valid)
# ============================================================


def validate_task_name(task_name):
    """
    Check if the task name is valid (non-empty).

    Parameters:
        task_name (str): The text entered by the user.

    Returns:
        tuple: (bool, str) — (is_valid, error_message)

    Example:
        >>> validate_task_name("")
        (False, "Please enter a task name before adding!")
        >>> validate_task_name("Math HW")
        (True, "")
    """
    if not task_name or task_name.strip() == "":
        return (False, "Please enter a task name before adding!")

    return (True, "")


def validate_task_selection(selected_items):
    """
    Check if the user has selected a task from the list.

    Parameters:
        selected_items (tuple): The selection from Treeview.selection()

    Returns:
        tuple: (bool, str) — (is_valid, error_message)
    """
    if not selected_items:
        return (False, "Please select a task first.")

    return (True, "")


def validate_tasks_exist(tasks_list):
    """
    Check if there are any tasks in the planner.

    Parameters:
        tasks_list (list): The current list of task dictionaries.

    Returns:
        tuple: (bool, str) — (is_valid, error_message)
    """
    if not tasks_list or len(tasks_list) == 0:
        return (False, "There are no tasks to process.")

    return (True, "")

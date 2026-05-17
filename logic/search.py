# ============================================================
# logic/search.py
# ============================================================
# This module provides search/filter functionality for tasks.
#
# HOW DYNAMIC SEARCH WORKS:
#   The GUI calls filter_tasks() every time the user types or
#   deletes a character in the search bar (bound to <KeyRelease>
#   event).  This gives a "live search" effect where results
#   update instantly as the user types.
#
#   The search is case-insensitive — typing "math" will match
#   "Math Assignment", "MATH HW", and "Advanced math".
# ============================================================


def filter_tasks(tasks, query):
    """
    Filter tasks whose name contains the search query.

    Parameters:
        tasks (list[dict]): The complete list of task dicts.
        query (str):        The search text entered by the user.

    Returns:
        list[dict]: A filtered list containing only tasks
                    whose "Task" field matches the query.

    The search is case-insensitive:
        - We convert both the task name and the query to
          lowercase before comparing.
        - The 'in' operator checks if query is a substring
          of the task name.

    Example:
        >>> tasks = [
        ...     {"Task": "Math HW", ...},
        ...     {"Task": "Science Project", ...},
        ... ]
        >>> filter_tasks(tasks, "math")
        [{"Task": "Math HW", ...}]
        >>> filter_tasks(tasks, "")
        [{"Task": "Math HW", ...}, {"Task": "Science Project", ...}]
    """

    # If the query is empty, return all tasks (no filtering)
    if not query or query.strip() == "":
        return tasks

    query_lower = query.lower().strip()

    # List comprehension — a compact way to filter a list
    # It reads as: "give me each task WHERE query is found
    #               inside the task name (case-insensitive)"
    filtered = [
        task for task in tasks
        if query_lower in task["Task"].lower()
    ]

    return filtered

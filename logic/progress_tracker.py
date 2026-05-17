from utils.constants import STATUS_COMPLETED


def calculate_progress(tasks):
    """
    Calculate task completion statistics.

    Parameters:
        tasks (list[dict]): The list of task dictionaries.

    Returns:
        dict: A dictionary with three keys:
              - "total"      (int)  : Total number of tasks
              - "completed"  (int)  : Number of completed tasks
              - "percentage" (float): Completion percentage (0-100)

    Formula:
        percentage = (completed / total) * 100
        If total is 0, percentage is 0 (avoids division by zero).

    Example:
        >>> tasks = [
        ...     {"Status": "Pending"},
        ...     {"Status": "Completed"},
        ...     {"Status": "Completed"},
        ... ]
        >>> calculate_progress(tasks)
        {"total": 3, "completed": 2, "percentage": 66.7}
    """
    total = len(tasks)

    # Count how many tasks have Status == "Completed"
    # sum() with a generator expression is a Pythonic way to count
    # items that match a condition.
    completed = sum(
        1 for task in tasks
        if task.get("Status") == STATUS_COMPLETED
    )

    # Calculate percentage (avoid division by zero)
    if total > 0:
        percentage = round((completed / total) * 100, 1)
    else:
        percentage = 0.0

    return {
        "total":      total,
        "completed":  completed,
        "percentage": percentage,
    }

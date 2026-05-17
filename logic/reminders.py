# ============================================================
# logic/reminders.py
# ============================================================
# This module checks task deadlines and generates reminder
# messages for tasks that are overdue, due today, or due
# within the next 2 days.
#
# HOW DEADLINE CHECKING WORKS:
#   1. Get today's date.
#   2. For each PENDING task, parse its deadline string into
#      a date object.
#   3. Subtract: days_left = (deadline - today).days
#      - Negative → OVERDUE
#      - Zero     → Due TODAY
#      - 1 or 2   → Deadline is NEAR
#   4. Collect all warning messages into a list and return it.
#
# WHY A SEPARATE MODULE?
#   The reminder logic is independent of the GUI.  By keeping
#   it here, we could reuse it in a command-line version or
#   even send email reminders in the future.
# ============================================================

from utils.helpers import parse_date, get_today
from utils.constants import STATUS_COMPLETED, REMINDER_DAYS_AHEAD


def check_deadlines(tasks):
    """
    Scan all pending tasks and return deadline warnings.

    Parameters:
        tasks (list[dict]): The list of task dictionaries.

    Returns:
        list[str]: A list of warning messages.
                   Empty list if no deadlines are approaching.

    Example return:
        [
            '🔴  "Math HW" is due TODAY!',
            '🟡  "Science" deadline is near (2 day(s) left)!',
            '⛔  "English" is OVERDUE (was due 3 day(s) ago)!',
        ]
    """
    today = get_today()
    reminders = []

    for task in tasks:
        # Skip tasks that are already completed
        if task["Status"] == STATUS_COMPLETED:
            continue

        # Parse the deadline string into a date object
        deadline = parse_date(task["Deadline"])

        # If the date couldn't be parsed, skip this task
        if deadline is None:
            continue

        # Calculate how many days until the deadline
        days_left = (deadline - today).days

        # Generate appropriate warning message
        if days_left < 0:
            # Task deadline has already passed
            reminders.append(
                f"⛔  \"{task['Task']}\" is OVERDUE "
                f"(was due {abs(days_left)} day(s) ago)!"
            )
        elif days_left == 0:
            # Task is due today
            reminders.append(
                f"🔴  \"{task['Task']}\" is due TODAY!"
            )
        elif days_left <= REMINDER_DAYS_AHEAD:
            # Task deadline is approaching (within 2 days)
            reminders.append(
                f"🟡  \"{task['Task']}\" deadline is near "
                f"({days_left} day(s) left)!"
            )

    return reminders

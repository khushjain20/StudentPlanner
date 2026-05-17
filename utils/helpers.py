# ============================================================
# utils/helpers.py
# ============================================================
# General-purpose helper/utility functions used across
# multiple modules in the project.
#
# These are small, standalone functions that don't belong
# to any specific feature but are useful everywhere.
# ============================================================

from datetime import datetime
from utils.constants import DATE_FORMAT


def format_date(date_obj):
    """
    Convert a Python date object to a formatted string.

    Parameters:
        date_obj (datetime.date): A date object.

    Returns:
        str: Date string in DD/MM/YYYY format.

    Example:
        >>> from datetime import date
        >>> format_date(date(2026, 5, 20))
        '20/05/2026'
    """
    return date_obj.strftime(DATE_FORMAT)


def parse_date(date_string):
    """
    Convert a date string (DD/MM/YYYY) back to a date object.

    Parameters:
        date_string (str): Date in DD/MM/YYYY format.

    Returns:
        datetime.date or None: Parsed date, or None if invalid.

    Example:
        >>> parse_date("20/05/2026")
        datetime.date(2026, 5, 20)
        >>> parse_date("invalid")
        None
    """
    try:
        return datetime.strptime(date_string, DATE_FORMAT).date()
    except (ValueError, TypeError):
        return None


def get_today():
    """
    Get today's date as a date object.

    Returns:
        datetime.date: Today's date.

    We wrap this in a function so that:
    1. Every module uses the same way to get "today".
    2. It's easier to test (we could mock this function).
    """
    return datetime.now().date()

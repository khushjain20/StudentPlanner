# ============================================================
# gui/widgets.py
# ============================================================
# Custom Tkinter widgets used in the project.
#
# Currently contains:
#   - PlaceholderEntry : A text entry box with "hint text"
#
# WHY CUSTOM WIDGETS?
#   Tkinter's built-in Entry widget doesn't support placeholder
#   text (the grey hint that disappears when you click).  By
#   creating our own class that EXTENDS tk.Entry, we add this
#   behaviour while keeping all the original Entry features.
#
# WHAT IS INHERITANCE?
#   PlaceholderEntry inherits from tk.Entry.  This means it
#   IS an Entry widget with extra features added on top.
#   We use super().__init__() to call the parent class's
#   constructor first, then add our custom logic.
# ============================================================

import tkinter as tk
from utils.constants import COLORS


class PlaceholderEntry(tk.Entry):
    """
    A text entry widget with placeholder (hint) text.

    HOW IT WORKS:
    ─────────────
    1. When created, we insert the placeholder text in grey.

    2. When the user CLICKS into the box (FocusIn event):
       → If the text is the placeholder → clear it
       → Change text colour to normal (white/light)

    3. When the user CLICKS AWAY (FocusOut event):
       → If the box is empty → restore the placeholder in grey

    This gives a modern "hint text" effect commonly seen in
    web forms and mobile apps.

    EVENTS USED:
    - <FocusIn>  : fires when the widget gains keyboard focus
    - <FocusOut> : fires when the widget loses keyboard focus

    Usage:
        entry = PlaceholderEntry(parent, placeholder="Type here...")
        actual_text = entry.get_value()  # returns "" if only placeholder
    """

    def __init__(self, master, placeholder="", **kwargs):
        """
        Parameters:
            master      : The parent widget (frame, window, etc.)
            placeholder : The hint text to show when empty.
            **kwargs    : Any other arguments passed to tk.Entry
                          (like font, bg, fg, width, etc.)
        """
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = COLORS["placeholder"]
        self.default_color = COLORS["text"]

        # Show the placeholder text initially
        self._show_placeholder()

        # Bind focus events to our handler methods
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _show_placeholder(self):
        """Insert the placeholder text in grey colour."""
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

    def _on_focus_in(self, event):
        """
        Called when the user clicks into the entry field.

        If the current text is the placeholder, we:
        1. Clear it (delete everything from position 0 to END)
        2. Switch text colour to the normal/default colour
        """
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_color)

    def _on_focus_out(self, event):
        """
        Called when the user clicks away from the entry field.

        If the field is now empty (user deleted everything),
        we restore the placeholder text in grey.
        """
        if self.get().strip() == "":
            self.delete(0, tk.END)
            self._show_placeholder()

    def get_value(self):
        """
        Get the actual text typed by the user.

        Returns:
            str: The user's input, stripped of whitespace.
                 Returns "" if only the placeholder is present.

        This is different from the built-in .get() method
        because .get() would return the placeholder text too.
        """
        current_text = self.get()
        if current_text == self.placeholder:
            return ""
        return current_text.strip()

    def clear_field(self):
        """
        Clear the entry and restore the placeholder.

        Called after successfully adding a task, so the field
        is ready for the next input.
        """
        self.delete(0, tk.END)
        self._show_placeholder()

from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *

class Bind:
    def __init__(self):
        self.window = Tk()
        self.window.title('Edit bindings')

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.force_close)

    def run_mainloop(self):
        self.window.mainloop()

    def save_close(self, command, action):
        """
        Saves changes to config.txt and deletes window.

        Parameters:
        command     target mind command
        action      keyboard action to be bound to `command`
        """
        change_bindings()

    def force_close(self):
        """
        Deletes window without saving changes.
        See `save_close` for window exit while retaining changes.
        """
        if tkinter.messagebox.askokcancel("Quit", "Are you sure that you want to exit? Changes will be not saved."):
            self.window.destroy()
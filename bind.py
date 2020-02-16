import tkinter as tk
import tkinter.messagebox

class Bind:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Edit bindings')
        
        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.force_close)

        self.window.mainloop()

    def save_close(self, param, value):
        change_bindings()

    def force_close(self):
        """
        Deletes window without saving changes.
        See `save_close` for window exit while retaining changes.
        """
        if tkinter.messagebox.askokcancel("Quit", "Are you sure that you want to exit? Changes will be not saved."):
            self.window.destroy()
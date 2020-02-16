from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *

class Bind:
    def __init__(self):
        self.bindings = [None, None, None, None]    # TODO: import existing bindings from config.txt
        self.window = Tk()

        # set window title
        self.window.title('Edit bindings')

        # hide maximize and minimize buttons
        self.window.attributes('-toolwindow', 1)

        # force window to stay on top
        self.window.attributes('-topmost', 1)

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.force_close)

        # profile selector (WIP)
        Label(self.window, text="Current profile:").grid(row=0, padx=5)
        self.profile = IntVar(self.window)
        self.profile_list = {1, 2, 3}   # BUG: option 1 does not appear in dropdown
        self.profile_sel = OptionMenu(self.window, self.profile, *self.profile_list)
        self.profile.set(1)
        self.profile_sel.configure(state=DISABLED)
        self.profile_sel.grid(row=0, column=1)

        # bindings menu
        for i in range(1, 4):
            Label(self.window, text="Command " + (str) (i)).grid(row=i, column=0, pady=10)
            Button(self.window, text="Train").grid(row=i, column=1)
            Entry(self.window, width=10).grid(row=i, column=2)
            Button(self.window, text="Re-bind").grid(row=i, column=3)

        # bottom buttons
        Button(self.window, text='Save and Exit', command=self.save_close(self.bindings)).grid(row=4, column=0, colspan=2)
        Button(self.window, text='Exit without saving', command=self.force_close()).grid(row=4, column=2, colspan=2)

    def run_mainloop(self):
        self.window.mainloop()

    def rebind(self, command):
        """
        Changes the keyboard binding associated with a command.

        Parameters:
        command     the command to be rebound
        """
        capture_input()
        reset_training()

    def train(self, command):
        """
        Initiates training of a command.

        Parameters:
        command     the command to be trained
        """
        start_training()

    def save_close(self, config):
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
        if askokcancel("Discard changes?", "Are you sure that you want to exit? Changes will be not saved.", icon=WARNING, default=CANCEL):
            self.window.destroy()
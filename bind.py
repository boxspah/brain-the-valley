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
        Button(self.window, text='Save and Exit', command=self.save_close).grid(row=4, column=0, columnspan=2)
        Button(self.window, text='Exit without saving', command=self.force_close).grid(row=4, column=2, columnspan=2)

    def run_mainloop(self):
        self.window.mainloop()

    def rebind(self, command):
        """
        Changes the keyboard binding associated with a command.

        Parameters:
        command     the command to be rebound
        """
        print("This will capture input")
        print("This will reset training data for this binding")

    def train(self, command):
        """
        Initiates training of a command.

        Parameters:
        command     the command to be trained
        """
        print("This will start a training session")

    def save_close(self):
        """
        Saves changes to config.txt and deletes window.
        """
        print("This will write the new bindings to config.txt")
        self.window.destroy()

    def force_close(self):
        """
        Deletes window without saving changes.
        See `save_close` for window exit while retaining changes.
        """
        if askokcancel("Discard changes?", "Are you sure that you want to exit? Changes will be not saved.", icon=WARNING, default=CANCEL):
            self.window.destroy()
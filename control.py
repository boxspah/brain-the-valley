from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
from cortex import Cortex

# external GUIs
from bind import Bind


class Control:
    def __init__(self):
        self.window = Tk()
        self.window.title('Wave.ly Control Panel')

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

    def setup(self, cortex):
        # connected headset info
        headset_id_label = LabelFrame(text='Current headset ID', relief=GROOVE)
        headset_id_display = Entry(headset_id_label, "", width=50)
        headset_id_display.insert(0, 'No headset connected')
        headset_id_display.config(state='readonly')
        headset_id_display.pack()
        headset_id_label.pack()

        buttons = Frame()
        connect = Button(buttons, text="Connect to headset", command=cortex.grant_access_and_session_info)
        connect.pack()
        edit_binds = Button(buttons, text="Edit bindings", command=self.edit)
        edit_binds.pack()
        terminate = Button(buttons, text="Exit", command=self.close)
        terminate.pack()
        buttons.pack(fill=BOTH)

        self.window.minsize(400, 300)

    def run_mainloop(self):
        self.window.mainloop()

    def edit(self):
        """
        Creates new window for user to access binding / training settings.

        Parameters:
        conn    connection variable
        """
        nw = Bind()

    def close(self):
        """
        Deletes main window and terminates program.
        """
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit? Wave.ly will stop running."):
            self.window.destroy()
            raise SystemExit('Program terminated by user')

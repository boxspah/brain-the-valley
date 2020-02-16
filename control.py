from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from cortex import Cortex

# external GUIs
from bind import Bind

class Control:
    def __init__(self):
        self.window = Tk()

        # disable maximize button
        self.window.resizable(0, 0)

        # set window title
        self.window.title('Wave.ly Control Panel')

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

    def setup(self, cortex):
        """
        Configure and create all widgets, and link connection to dialog.
        """
        # set default styling for buttons
        Style().configure('TButton', padding=7, relief='flat')
        
        # display connected headset info
        headset_id_label = LabelFrame(text='Current headset ID', relief=GROOVE)
        headset_id_display = Entry(headset_id_label, width=50)
        headset_id_display.insert(0, 'No headset connected')
        headset_id_display.config(state='readonly')
        headset_id_display.pack()
        headset_id_label.pack(expand=1)

        # actions menu
        buttons = Frame()
        connect = Button(buttons, text="Connect to headset", command=cortex.grant_access_and_session_info).pack(pady=7)
        Button(buttons, text="Edit bindings", command=self.edit).pack(pady=7)
        Button(buttons, text="Exit", command=self.close).pack(pady=7)
        buttons.pack(fill=BOTH, anchor=CENTER, expand=1)

        # set minimum window size to 400x300
        self.window.minsize(400, 300)

        self.window.mainloop()

    def edit(self):
        """
        Creates new window for user to access binding / training settings.
        """
        nw = Bind()
        nw.run_mainloop()

    def close(self):
        """
        Deletes main window and terminates program.
        """
        if askokcancel("Quit Wave.ly?", "Are you sure you want to quit? Wave.ly will stop running.", icon=WARNING, default=CANCEL):
            self.window.destroy()
            raise SystemExit('Program terminated by user')

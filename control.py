import tkinter as tk
import tkinter.messagebox
from cortex import Cortex

# external GUIs
from bind import Bind

class Control:
    def __init__(self):
        connection_url = "wss://localhost:6868"
        user = {
            "client_id": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
            "client_secret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
            "license": "",
            "debit": 500,
        }
        self.headset = Cortex(connection_url,user)

        self.window = tk.Tk()
        self.window.title('Wave.ly Control Panel')

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        # connected headset info
        self.headset_id = None
        headset_id_label = tk.LabelFrame(text='Current headset ID', bd=3, relief=tk.GROOVE, padx=10, pady=5)
        headset_id_display = tk.Entry(headset_id_label, self.headset_id, width=50)
        headset_id_display.insert(0, 'No headset connected')
        headset_id_display.config(state='readonly')
        headset_id_display.pack()
        headset_id_label.pack(padx=5)


        buttons = tk.Frame(padx=10, pady=10)
        connect = tk.Button(buttons, text="Connect to headset", command=self.connect)
        connect.pack()
        edit_binds = tk.Button(buttons, text="Edit bindings", command=self.edit)
        edit_binds.pack()
        terminate =  tk.Button(buttons, text="Exit", command=self.close)
        terminate.pack()
        buttons.pack(fill=tk.BOTH)

        self.window.minsize(400, 300)
        self.window.mainloop()

    def connect(self):
        """
        Initiates connection with headset through connect.py.

        Returns connection variable.
        """
        self.headset.grant_access_and_session_info()

    def edit(self, conn):
        """
        Creates new window for user to access binding / training settings.

        Parameters:
        conn    connection variable
        """
        nw = Bind(conn)

    def close(self):
        """
        Deletes main window and terminates program.
        """
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit? Wave.ly will stop running."):
            self.window.destroy()
            raise SystemExit('Program terminated by user')
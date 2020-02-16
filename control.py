from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from cortex import Cortex
from scipy.spatial.transform import Rotation as R
from pynput import mouse, keyboard
from helper import *

# external GUIs
from bind import Bind

class Control:
    def __init__(self):
        self.ms = mouse.Controller()
        self.ms_list = []
        self.ms_pos = (0, 0)
        self.zero_pos = [0, 0, 0]
        self.rot = [0, 0, 0]

        connection_url = "wss://localhost:6868"
        user = {
            "client_id": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
            "client_secret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
            "license": "",
            "debit": 500
        }
        self.cortex = Cortex(connection_url, user)
        self.window = Tk()

        self.screen_w, self.screen_h = 1920, 1080
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()
        self.prev = [self.screen_h / 2, self.screen_w / 2, 0]
        self.ms.position = (0, 0)

        # disable maximize button
        self.window.resizable(0, 0)

        # set window title
        self.window.title('Wave.ly Control Panel')

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        # set default styling for buttons
        Style().configure('TButton', padding=7, relief='flat')
        
        # display connected headset info
        headset_id_label = LabelFrame(self.window, text='Current headset ID', relief=GROOVE)
        headset_id_display = Entry(headset_id_label, width=50)
        headset_id_display.insert(0, 'No headset connected')
        headset_id_display.config(state='readonly')
        headset_id_display.pack()
        headset_id_label.pack(expand=1)

        # actions menu
        buttons = Frame()
        connect = Button(buttons, text="Connect to headset", command=self.connect_to_headset).pack(pady=7)
        Button(buttons, text="Edit bindings", command=self.edit).pack(pady=7)
        Button(buttons, text="Exit", command=self.close).pack(pady=7)
        buttons.pack(fill=BOTH, anchor=CENTER, expand=1)

        # set minimum window size to 400x300
        self.window.minsize(400, 300)

        self.window.mainloop()

    def on_press(self, key):
        if key=='a':
            exit(0)

    def on_release(self, key):
        if key == keyboard.Key.space:
            self.zero_pos = self.rot
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def motion_sensor(self):
        signal = self.cortex.recieve_signal()
        if list(signal.keys())[0] == 'mot':
            quaternion = signal["mot"][2:6]
            r = R.from_quat(quaternion)
            self.rot = list(map(lambda x: x if x > 0 else x + 360, r.as_euler('xzy', degrees=True)))
            conv = [scale(
                clamp(self.rot[0], self.zero_pos[0], self.zero_pos[0] - 14),
                self.zero_pos[0],
                self.zero_pos[0] - 14,
                0,
                self.screen_w
            ),
                scale(
                    clamp(self.rot[1], self.zero_pos[1], self.zero_pos[1] - 7),
                    self.zero_pos[1],
                    self.zero_pos[1] - 7,
                    self.screen_h,
                    0
                )
            ]

            conv = list(map(lambda x: int(x), conv))
            self.prev = ema_filter(conv, self.prev, [0.95, 0.95, 0.7])
            self.ms_list.append(self.prev)
            n=5
            l = 5
            if len(self.ms_list)>=  n:
                self.ms.position = [(sum(x for x,y in self.ms_list)/n)//l *l , (sum(y for x,y in self.ms_list)/n)//l*l]
                self.ms_list.pop(0)

            print(self.ms.position)
                # ms_list.pop(0)wwww
        elif list(signal.keys())[0] == "com":
            mental_cmd = signal["com"]
            if mental_cmd[0] == "push":
                self.ms.click(mouse.Button.left)
                print("moving")
            #elif mental_cmd[0] == "lift":
            #   ms.click(Button.left)
            #  print("clicking")
        self.window.after(0, self.motion_sensor)
    
    def update_window(self):
        self.window.update_idletasks()
        self.window.update()

    def connect_to_headset(self):
        """
        Initiates connection to Emotiv headset and stores connection object in Control.
        """
        self.cortex.grant_access_and_session_info()
        self.cortex.guest_profile()
        self.cortex.subRequest(['mot', 'sys'])
        self.motion_sensor()

    def edit(self):
        """
        Creates new window for user to access binding / training settings.
        """
        nw = Bind(self.cortex)

    def close(self):
        """
        Deletes main window and terminates program.
        """
        if askokcancel("Quit Wave.ly?", "Are you sure you want to quit? Wave.ly will stop running.", icon=WARNING, default=CANCEL):
            self.window.destroy()
            raise SystemExit('Program terminated by user')

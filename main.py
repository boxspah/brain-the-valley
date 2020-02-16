from control import Control
from cortex import Cortex
from scipy.spatial.transform import Rotation as R
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import json
from helper import *
import time
from win32api import GetSystemMetrics
screen_w, screen_h = GetSystemMetrics(0), GetSystemMetrics(1)
connection_url = "wss://localhost:6868"
user = {
    "client_id": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
    "client_secret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
    "license": "",
    "debit": 500
}

headset = Cortex(connection_url, user)


main = Control()
main.setup(headset)
main.run_mainloop()
headset.setup_profile("Asad")
headset.subRequest(["mot"])

ms = Controller()

zero_pos = [0, 0, 0]
rot = [0, 0, 0]


def on_press(key):
    return None


def on_release(key):
    if key == keyboard.Key.space:
        global zero_pos
        zero_pos = rot
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
prev = [screen_h / 2, screen_w / 2, 0]
ms.position = (0, 0)

while True:
    signal = headset.recieve_signal()
    quaternion = signal["mot"][2:6]
    r = R.from_quat(quaternion)
    rot = list(map(lambda x: x if x > 0 else x + 360, r.as_euler('xzy', degrees=True)))
    print("rot", rot, end=' ')
    conv = [scale(
        clamp(rot[0], zero_pos[0], zero_pos[0] - 14),
        zero_pos[0],
        zero_pos[0] - 14,
        0,
        screen_w
    ),
        scale(
            clamp(rot[1], zero_pos[1], zero_pos[1] - 7),
            zero_pos[1],
            zero_pos[1] - 7,
            screen_h,
            0
        ),
        0
    ]
    conv = list(map(lambda x: int(x), conv))
    print("conv", conv)
    prev = ema_filter(conv, prev, [0.7, 0.7, 0.7])

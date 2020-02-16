from control import Control
from cortex import Cortex
from scipy.spatial.transform import Rotation as R
from pynput import mouse,keyboard
from pynput.mouse import Button, Controller
import keyboard as kb
import asyncio
import json
from helper import *
import time

screen_w, screen_h = 1366, 768
connection_url = "wss://localhost:6868"
user = {
    "client_id": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
    "client_secret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
    "license": "",
    "debit": 500
}

headset = Cortex(connection_url, user)
# headset.grant_access_and_session_info()

main = Control()
main.setup(headset)
headset.setup_profile("Asad")
headset.subRequest(["com", "mot"])


ms = Controller()


zero_pos = [0, 0, 0]
rot = [0, 0, 0]


def on_press(key):
    if key== 'a':
        exit(0)


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
prev = [screen_h / 2, screen_w / 2]
ms.position = (0, 0)
ms_list = []
while True:
    main.loop()
    signal = headset.recieve_signal()
    if list(signal.keys())[0] == 'mot':
        quaternion = signal["mot"][2:6]
        r = R.from_quat(quaternion)
        rot = list(map(lambda x: x if x > 0 else x + 360, r.as_euler('xzy', degrees=True)))
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
            )
        ]

        conv = list(map(lambda x: int(x), conv))
        prev = ema_filter(conv, prev, [0.7, 0.7, 0.7])
        ms_list.append(prev)
        n=5
        l = 20
        if len(ms_list)>=  n:
            ms.position = [(sum(x for x,y in ms_list)/n)//l *l , (sum(y for x,y in ms_list)/n)//l*l]
            ms_list.pop(0)

        print(ms.position)
            # ms_list.pop(0)wwww
    elif list(signal.keys())[0] == "com":
        mental_cmd = signal["com"]
        if mental_cmd[0] == "push":
            ms.click(Button.left)
            print("moving")
        #elif mental_cmd[0] == "lift":
         #   ms.click(Button.left)
          #  print("clicking")

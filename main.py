from control import Control
from cortex import Cortex
from scipy.spatial.transform import Rotation as R
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import json
from helper import *
import input
connection_url = "wss://localhost:6868"
user = {
    "client_id": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
    "client_secret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
    "license": "",
    "debit": 500
}
headset = Cortex(connection_url, user)
headset.grant_access_and_session_info()
headset.setup_profile("Asad")
headset.subRequest(["mot"])

ms = Controller()


prev = [input.screen_h/2, input.screen_w/2,0]
while True:
    signal = headset.recieve_signal()
    quaternion = signal["mot"][2:6]
    r = R.from_quat(quaternion)
    input.rot = r.as_euler('xzy', degrees=True)
    print(input.rot, end=' ')
    input.rot = [
        clamp(
            scale(
                input.rot[0],
                zero_pos[0],
                zero_pos[0]-10,
                0,
                screen_w
            ), 0, screen_w
        ),
        clamp(
            scale(
                input.rot[1],
                zero_pos[1],
                zero_pos[1]+15,
                0,
                screen_h
            ), 0, screen_h
        ),
        0
    ]
    print(prev)
    prev = ema_filter(input.rot, prev, [0.2,0.2,0.2])



main = Control()
main.setup(headset)


# main.run_mainloop()

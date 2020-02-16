from control import Control
from cortex import Cortex
from scipy.spatial.transform import Rotation as R
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import json
from helper import *
import time

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

zero_pos = [0, 0, 0]
screen_w = 1920
screen_h = 1080
rot = [0, 0, 0]
def on_press(key):
    try:

        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(
        key))

    if key == keyboard.Key.space:
        global zero_pos
        zero_pos= rot
    if key == keyboard.Key.esc:
        # Stop listener
        return False



# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
prev = [screen_h/2, screen_w/2,0]
ms_list = []
ms.position = (0, 0)
while True:

    signal = headset.recieve_signal()
    quaternion = signal["mot"][2:6]
    r = R.from_quat(quaternion)
    rot = list(map(lambda x: x if x>0 else x+360, r.as_euler('xzy', degrees=True)))
    print("rot", rot,end=' ')
    conv = [scale(
                clamp(rot[0],zero_pos[0],zero_pos[0]-14),
                zero_pos[0],
                zero_pos[0]-14,
                0,
                screen_w
            ),
            scale(
                clamp(rot[1],zero_pos[1] ,zero_pos[1]-7),
                zero_pos[1],
                zero_pos[1]-7,
                screen_h,
                0
            ),
        0
        ]
    conv = list(map(lambda x: int(x), conv))
    print("conv", conv)
    prev = ema_filter(conv, prev, [0.7,0.7,0.7])

    ms_list.append(tuple(conv[0:2]))
    if len(ms_list) > 6:
        ms.position = (sum(x for x,y in ms_list)/6, sum(y for x, y in ms_list)/6 )
        ms_list.pop(0)



main = Control()
main.setup(headset)


# main.run_mainloop()

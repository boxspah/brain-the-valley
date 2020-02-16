from pynput import keyboard

zero_pos = [0, 0, 0]
screen_w = 1920
screen_h = 1080
rot = [0, 0, 0]
def on_press(key):
    if key == Key.space:
        zero_pos = rot


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
#mport eeg
import keyboard as kb

kb.add_hotkey('a', lambda: keyboard.write('Geek'))
kb.add_hotkey('ctrl + shift + a', print, args=('you entered', 'hotkey'))

kb.wait('esc')
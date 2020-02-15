import tkinter as tk
import tkinter.messagebox

class Control:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Wave.ly Control Panel')
        
        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        self.window.mainloop()

    def close(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit? Wave.ly will stop running."):
            self.window.destroy()
            raise SystemExit('Program terminated by user')
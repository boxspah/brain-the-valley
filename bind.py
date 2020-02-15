import tkinter as tk
import tkinter.messagebox

class Control:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Edit bindings')
        
        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        self.window.mainloop()

    def close(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure that you want to exit? Changes will be not saved."):
            self.window.destroy()
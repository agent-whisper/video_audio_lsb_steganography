import tkinter as tk

from pages.mainmenu import MainMenu

class App(tk.Tk):
    def __init__(self, title='window', width='500', height='300', resizable=True):
        tk.Tk.__init__(self)
        self.title('Tugas Besar 1')
        window_width = str(width)
        window_height= str(height)
        self.geometry('{}x{}'.format(window_width,window_height))
        
        self._frame = None
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(relx=0.5, rely=0.1, y=48, anchor=tk.CENTER)
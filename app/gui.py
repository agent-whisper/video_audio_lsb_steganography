import tkinter as tk
import app.pages.mainmenu as mainmenu
import app.pages.video.insertion as vid_insert
import app.pages.video.extraction as vid_extract
import app.pages.audio.insertion as audio_insert
import app.pages.audio.extraction as audio_extract
import app.pages.audio.insertion_result as audio_ins_result

class App(tk.Tk):
    def __init__(self, title='window', width='800', height='600', resizable=True):
        tk.Tk.__init__(self)
        self.title('Tugas Besar 1')
        window_width = str(width)
        window_height= str(height)
        self.geometry('{}x{}'.format(window_width,window_height))

        self._frame = None
        self.open_main_menu()

    def open_main_menu(self):
        self.replace_frame(mainmenu.MainMenu)
    
    def open_hide_vid_form(self):
        self.replace_frame(vid_insert.VideoInsertionForm)

    def open_extract_vid_form(self):
        self.replace_frame(vid_extract.VideoExtractionForm)

    def open_hide_audio_form(self):
        self.replace_frame(audio_insert.AudioInsertionForm)

    def open_extract_audio_form(self):
        self.replace_frame(audio_extract.AudioExtractionForm)

    def open_hide_audio_result(self, result):
        new_frame = audio_ins_result.AudioInsertionResult(self, result)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(relx=0.5, y=48, anchor=tk.N)

    def replace_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(relx=0.5, y=48, anchor=tk.N)
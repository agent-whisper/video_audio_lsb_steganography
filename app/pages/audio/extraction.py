import time

import tkinter as tk
import tkinter.filedialog as tkfd
import vlc

class AudioExtractionForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.TITLE_ROW = 0
        self.SELECT_AUDIO_ROW = 1
        self.KEY_ENTRY_ROW = 2

        tk.Label(self, text='Ekstraksi Audio', font='none 24 bold').grid(row=self.TITLE_ROW, column=1, columnspan=2, sticky=tk.W+tk.E)
        
        # Pilih stego-audio
        self.audio_dir = tk.StringVar()
        self.audio_dir.set('')
        self.render_file_select_frame()

        # Input Stegano Key
        key_label = tk.Label(self, text='Stegano Key:')
        key_label.grid(row=self.KEY_ENTRY_ROW, column=0, sticky=tk.W)
        key_entry = tk.Entry(self)
        key_entry.grid(row=self.KEY_ENTRY_ROW, column=1)

        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(self, text='Eksekusi')
        execute_button.grid(row=self.KEY_ENTRY_ROW+1, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.KEY_ENTRY_ROW+1, column=1)

    def render_file_select_frame(self):
        select_vid_dialog_frame = tk.Frame(self)
        select_vid_dialog_frame.grid(row=self.SELECT_AUDIO_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=select_vid_dialog_frame, text='Stego Audio:').grid(row=0, sticky=tk.W)
        vid_input_label = tk.Label(master=select_vid_dialog_frame, textvariable=self.audio_dir)
        vid_input_label.grid(row=1, columnspan=2, sticky=tk.W)
        pick_cv_button = tk.Button(
            master=select_vid_dialog_frame,
            text='Pilih',
            command = lambda: self.load_audio_file(),
        )
        pick_cv_button.grid(row=2, column=0, sticky=tk.W)
        preview_cv_button = tk.Button(
            master=select_vid_dialog_frame,
            text='Buka Audio',
            command= lambda: self.play_audio(),
        )
        preview_cv_button.grid(row=2, column=1, sticky=tk.W)

    def load_audio_file(self):
        self.audio_dir.set(tkfd.askopenfilename(filetypes=(
            (".WAV Audio", "*.wav"),
        )))

    def play_audio(self):
        player = vlc.MediaPlayer(self.audio_dir.get())
        try:
            player.play()
            time.sleep(0.5)
            duration = player.get_length() / 1000
            time.sleep(duration)
            time.sleep(0.5)
        except vlc.VLCException as e:
            print(e)
        finally:
            player.stop()
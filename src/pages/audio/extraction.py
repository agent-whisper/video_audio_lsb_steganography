import time

import src.steganography.audio.lsb.api as alsb_api
import tkinter as tk
import tkinter.filedialog as tkfd
import vlc

class AudioExtractionForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.DEFAULT_OUT_FILENAME = 'audio_extraction_result'
        self.TITLE_ROW = 0
        self.SELECT_AUDIO_ROW = 1
        self.KEY_ENTRY_ROW = 2
        self.SAVEAS_ROW = 3
        self.EXECUTE_ROW = 4

        tk.Label(self, text='Ekstraksi Audio', font='none 24 bold').grid(row=self.TITLE_ROW, column=1, columnspan=2, sticky=tk.W+tk.E)
        
        # Pilih stego-audio
        self.audio_dir = tk.StringVar()
        self.audio_dir.set('')
        self.is_mono = False
        self.render_file_select_frame()

        # Input Stegano Key
        key_label = tk.Label(self, text='Stegano Key:')
        key_label.grid(row=self.KEY_ENTRY_ROW, column=0, sticky=tk.W)
        key_entry = tk.Entry(self)
        key_entry.grid(row=self.KEY_ENTRY_ROW, column=1)

        # Entri untuk nama file output
        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)
        saveas_dialog_frame = tk.Frame(self)
        saveas_dialog_frame.grid(row=self.SAVEAS_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=saveas_dialog_frame, text='Nama file output (tanpa ekstensi):').grid(row=0, column=0, columnspan=2, sticky=tk.W)
        saveas_entry = tk.Entry(master=saveas_dialog_frame)
        saveas_entry.grid(row=1, column=0, sticky=tk.W)
        saveas_entry.insert(tk.END, self.DEFAULT_OUT_FILENAME)

        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(
            self,
            text='Eksekusi',
            command=lambda: self.execute(master, key_entry.get(), saveas_entry.get()),
        )
        execute_button.grid(row=self.EXECUTE_ROW, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.EXECUTE_ROW, column=1)

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
        self.is_mono = (alsb_api.check_is_mono(self.audio_dir.get()) == 1)

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

    def execute(self, master, key, output_filename):
        # result = {
        #     'result' : 'debug',
        #     'output_dir' : '/home/fariz/Documents/kuliah/semester8/kripto/tubes1/Yamaha-V50-Rock-Beat-120bpm.wav',
        # }
        if self.audio_dir.get() == '' or key == '' or output_filename == '':
            return
    
        result = alsb_api.extract_message(
            self.audio_dir.get(),
            key,
            output_filename,
            self.is_mono
        )
        print('Extraction Finished!')
        master.open_extract_audio_result(result)
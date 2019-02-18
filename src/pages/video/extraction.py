import time

import src.steganography.video.lsb as vlsb
import tkinter as tk
import tkinter.filedialog as tkfd
import  vlc

class VideoExtractionForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.TITLE_ROW = 0
        self.SELECT_VID_ROW = 1
        self.KEY_ENTRY_ROW = 2
        self.SAVEAS_ROW = 3
        self.EXECUTE_ROW = 4
        self.DEFAULT_OUT_FILENAME = 'video_extraction_result'

        tk.Label(self, text='Ekstraksi Video', font='none 24 bold').grid(row=self.TITLE_ROW, column=1, columnspan=2, sticky=tk.W+tk.E)
        
        # Pilih stego-video
        self.video_dir = tk.StringVar()
        self.video_dir.set('')
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
        tk.Label(master=saveas_dialog_frame, text='Save as:').grid(row=0, column=0, columnspan=2, sticky=tk.W)
        saveas_entry = tk.Entry(master=saveas_dialog_frame)
        saveas_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(self, text='Eksekusi', command=lambda: self.execute(master, key_entry.get(), saveas_entry.get()))
        execute_button.grid(row=self.EXECUTE_ROW, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.EXECUTE_ROW, column=1)

    def render_file_select_frame(self):
        select_vid_dialog_frame = tk.Frame(self)
        select_vid_dialog_frame.grid(row=self.SELECT_VID_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=select_vid_dialog_frame, text='Stego Video:').grid(row=0, sticky=tk.W)
        vid_input_label = tk.Label(master=select_vid_dialog_frame, textvariable=self.video_dir)
        vid_input_label.grid(row=1, columnspan=2, sticky=tk.W)
        pick_cv_button = tk.Button(
            master=select_vid_dialog_frame,
            text='Pilih',
            command = lambda: self.load_video_file(),
        )
        pick_cv_button.grid(row=2, column=0, sticky=tk.W)
        preview_cv_button = tk.Button(
            master=select_vid_dialog_frame,
            text='Buka Video',
            command= lambda: self.play_video(),
        )
        preview_cv_button.grid(row=2, column=1, sticky=tk.W)

    def load_video_file(self):
        self.video_dir.set(tkfd.askopenfilename(filetypes=(
            (".AVI Videos", "*.avi"),
        )))

    def play_video(self):
        player = vlc.MediaPlayer(self.video_dir.get())
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
        #     'output_dir' : '/home/fariz/Documents/kuliah/semester8/kripto/tubes1/flame.avi',
        # }
        if self.video_dir == '' or key == '' or output_filename == '':
            return
        print('--- Executing Video LSB Extraction ---')
        print('Video file: {}'.format(self.video_dir.get()))
        print('Key: {}'.format(key))
        result = vlsb.extract_secret(self.video_dir.get(), key, output_filename)
        master.open_extract_video_result(result)
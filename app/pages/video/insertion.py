import time

import tkinter as tk
import tkinter.filedialog as tkfd
import vlc

class VideoInsertionForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.LSB_MODES = [
            ('Sequential', 'seq'),
            ('Randomized', 'ran'),
        ]
        self.RANDOM_OPTIONS = [
            ('Byte'),
            ('Frame'),
        ]
        self.TITLE_ROW = 0
        self.COVER_FILE_ROW = 1
        self.SECRET_MESSAGE_ROW = 2
        self.KEY_ENTRY_ROW = 3
        self.OPTIONS_ROW = 4

        # Judul Halaman
        tk.Label(self, text='Steganografi Video', font='none 24 bold').grid(row=self.TITLE_ROW, columnspan=2, sticky=tk.W+tk.E)

        # Input cover file dan playback
        self.cover_file_dir = tk.StringVar()
        self.cover_file_dir.set('')
        self.render_cover_file_frame()

        # Input lokasi file rahasia
        self.secret_message_dir = tk.StringVar()
        self.secret_message_dir.set('')
        self.render_secret_message_frame()        

        # Input Stegano Key
        key_label = tk.Label(self, text='Stegano Key:')
        key_label.grid(row=self.KEY_ENTRY_ROW, column=0, sticky=tk.W)
        key_entry = tk.Entry(self)
        key_entry.grid(row=self.KEY_ENTRY_ROW, column=1)

        # Opsi untuk mode LSB
        self.lsb_mode = tk.StringVar()
        self.lsb_mode.set('seq')
        self.rand_options = {}
        self.render_lsb_options_frame()
        
        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(self, text='Eksekusi')
        execute_button.grid(row=self.OPTIONS_ROW+1, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.OPTIONS_ROW+1, column=1)
    
    def render_cover_file_frame(self):
        cv_dialog_frame = tk.Frame(self)
        cv_dialog_frame.grid(row=self.COVER_FILE_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=cv_dialog_frame, text='Cover Video:').grid(row=0, sticky=tk.W)
        cv_input_label = tk.Label(master=cv_dialog_frame, textvariable=self.cover_file_dir)
        cv_input_label.grid(row=1, columnspan=2, sticky=tk.W)
        pick_cv_button = tk.Button(
            master=cv_dialog_frame,
            text='Pilih',
            command = lambda: self.load_video_file(),
        )
        pick_cv_button.grid(row=2, column=0, sticky=tk.W)
        preview_cv_button = tk.Button(
            master=cv_dialog_frame,
            text='Buka Video',
            command= lambda: self.play_video(),
        )
        preview_cv_button.grid(row=2, column=1, sticky=tk.W)

    def render_secret_message_frame(self):
        msg_dialog_frame = tk.Frame(self)
        msg_dialog_frame.grid(row=self.SECRET_MESSAGE_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=msg_dialog_frame, text='Berkas Rahasia:').grid(row=0, sticky=tk.W)
        msg_input_label = tk.Label(master=msg_dialog_frame, textvariable=self.secret_message_dir)
        msg_input_label.grid(row=1, columnspan=2, sticky=tk.W)
        pick_msg_button = tk.Button(
            master=msg_dialog_frame,
            text='Pilih',
            command = lambda: self.load_secret_message(),
        )
        pick_msg_button.grid(row=2, sticky=tk.W)

    def load_video_file(self):
        self.cover_file_dir.set(tkfd.askopenfilename(filetypes=(
            (".AVI Videos", "*.avi"),
        )))

    def load_secret_message(self):
        self.secret_message_dir.set(tkfd.askopenfilename())

    def play_video(self):
        player = vlc.MediaPlayer(self.cover_file_dir.get())
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

    def render_lsb_options_frame(self):
        options_frame = tk.Frame(self)
        options_frame.grid(row=self.OPTIONS_ROW, column=0, sticky=tk.W+tk.E)
        row_offset = 0
        for label, mode in self.LSB_MODES:
            b = tk.Radiobutton(
                master=options_frame,
                text=label,
                variable=self.lsb_mode,
                value=mode
            )
            b.grid(row=row_offset, column=0, sticky=tk.W)
            row_offset += 1

        row_offset = 0
        for label in self.RANDOM_OPTIONS:
            self.rand_options[label] = tk.StringVar()
            b = tk.Checkbutton(
                master=options_frame,
                text=label,
                variable=self.rand_options[label]
            )
            b.grid(row=row_offset, column=1, sticky=tk.W)
            row_offset += 1
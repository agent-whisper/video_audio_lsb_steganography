import tkinter as tk
import tkinter.filedialog as tkfd

class VideoInsertionForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        LSB_MODES = [
            ('Sequential', 'seq'),
            ('Randomized', 'ran'),
        ]
        RANDOM_OPTIONS = [
            ('Byte'),
            ('Frame'),
        ]
        TITLE_ROW = 0
        COVER_FILE_ROW = 1
        SECRET_MESSAGE_ROW = 2
        KEY_ENTRY_ROW = 3
        OPTIONS_ROW = 4

        # Judul Halaman
        tk.Label(self, text='Steganografi Video', font='none 24 bold').grid(row=TITLE_ROW, columnspan=2, sticky=tk.W+tk.E)

        # Input lokasi file cover
        self.cover_file_dir = tk.StringVar()
        self.cover_file_dir.set('')
        cv_dialog_frame = tk.Frame(self)
        cv_dialog_frame.grid(row=COVER_FILE_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
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
            # command=,
        )
        preview_cv_button.grid(row=2, column=1, sticky=tk.W)

        # Input lokasi file rahasia
        self.secret_message_dir = tk.StringVar()
        self.secret_message_dir.set('')
        msg_dialog_frame = tk.Frame(self)
        msg_dialog_frame.grid(row=SECRET_MESSAGE_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=msg_dialog_frame, text='Berkas Rahasia:').grid(row=0, sticky=tk.W)
        msg_input_label = tk.Label(master=msg_dialog_frame, textvariable=self.secret_message_dir)
        msg_input_label.grid(row=1, columnspan=2, sticky=tk.W)
        pick_msg_button = tk.Button(
            master=msg_dialog_frame,
            text='Pilih',
            command = lambda: self.load_secret_message(),
        )
        pick_msg_button.grid(row=2, sticky=tk.W)

        # Input Stegano Key
        key_label = tk.Label(self, text='Stegano Key:')
        key_label.grid(row=KEY_ENTRY_ROW, column=0, sticky=tk.W)
        key_entry = tk.Entry(self)
        key_entry.grid(row=KEY_ENTRY_ROW, column=1)

        # Opsi untuk mode LSB
        options_frame = tk.Frame(self)
        options_frame.grid(row=OPTIONS_ROW, column=0, sticky=tk.W+tk.E)
        lsb_mode = tk.StringVar()
        lsb_mode.set('seq')
        row_offset = 0
        for label, mode in LSB_MODES:
            b = tk.Radiobutton(
                master=options_frame,
                text=label,
                variable=lsb_mode,
                value=mode
            )
            b.grid(row=row_offset, column=0, sticky=tk.W)
            row_offset += 1

        rand_options = {}
        row_offset = 0
        for label in RANDOM_OPTIONS:
            rand_options[label] = tk.StringVar()
            b = tk.Checkbutton(
                master=options_frame,
                text=label,
                variable=rand_options[label]
            )
            b.grid(row=row_offset, column=1, sticky=tk.W)
            row_offset += 1

        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(self, text='Eksekusi')
        execute_button.grid(row=OPTIONS_ROW+1, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=OPTIONS_ROW+1, column=1)
    
    def load_video_file(self):
        self.cover_file_dir.set(tkfd.askopenfilename(filetypes=(
            (".AVI Videos", "*.avi"),
        )))

    def load_secret_message(self):
        self.secret_message_dir.set(tkfd.askopenfilename())
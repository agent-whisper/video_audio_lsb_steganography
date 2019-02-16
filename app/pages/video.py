import tkinter as tk

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

        # Tombol kembali
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=OPTIONS_ROW+1, column=0, columnspan=2)
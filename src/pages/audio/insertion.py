import time

import tkinter as tk
import tkinter.filedialog as tkfd
import src.steganography.audio.lsb.api as alsb_api
import vlc

class AudioInsertionForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.LSB_MODES = [
            ('1-bit', 1),
            ('2-bit', 2),
        ]
        self.RANDOM_OPTIONS = [
            ('Random Byte'),
            ('Random Frame'),
        ]
        self.DEFAULT_OUT_FILENAME = 'audio_insertion_result'
        self.TITLE_ROW = 0
        self.COVER_FILE_ROW = 1
        self.SECRET_MESSAGE_ROW = 2
        self.KEY_ENTRY_ROW = 3
        self.OPTIONS_ROW = 4
        self.SAVEAS_ROW = 5
        self.EXECUTE_ROW = 6

        # Judul Halaman
        tk.Label(self, text='Steganografi Audio', font='none 24 bold').grid(row=self.TITLE_ROW, columnspan=2, sticky=tk.W+tk.E)

        # Input cover file dan playback
        self.cover_file_dir = tk.StringVar()
        self.cover_file_dir.set('')
        self.is_mono = False
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
        self.lsb_bit_mode = tk.IntVar()
        self.lsb_bit_mode.set(1)
        self.rand_options = {}
        for mode in self.RANDOM_OPTIONS:
            self.rand_options[mode] = tk.IntVar()
            self.rand_options[mode].set(0)
        self.use_encryption = tk.IntVar()
        self.use_encryption.set(0)
        self.options_frame = tk.Frame(self)
        self.options_buttons = {}
        self.render_lsb_options_frame()
        
        # Entri untuk nama file output
        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)
        saveas_dialog_frame = tk.Frame(self)
        saveas_dialog_frame.grid(row=self.SAVEAS_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=saveas_dialog_frame, text='Nama file output:').grid(row=0, column=0, columnspan=2, sticky=tk.W)
        saveas_entry = tk.Entry(master=saveas_dialog_frame)
        saveas_entry.grid(row=1, column=0, sticky=tk.W)
        saveas_entry.insert(tk.END, self.DEFAULT_OUT_FILENAME)
        tk.Label(master=saveas_dialog_frame, text='.wav').grid(row=1, column=1, sticky=tk.W)

        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(self, text='Eksekusi', command=lambda: self.execute(master, key_entry.get(), saveas_entry.get()))
        execute_button.grid(row=self.EXECUTE_ROW, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.EXECUTE_ROW, column=1)
    
    def render_cover_file_frame(self):
        ca_dialog_frame = tk.Frame(self)
        ca_dialog_frame.grid(row=self.COVER_FILE_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        tk.Label(master=ca_dialog_frame, text='Cover Audio:').grid(row=0, sticky=tk.W)
        cv_input_label = tk.Label(master=ca_dialog_frame, textvariable=self.cover_file_dir)
        cv_input_label.grid(row=1, columnspan=2, sticky=tk.W)
        pick_cv_button = tk.Button(
            master=ca_dialog_frame,
            text='Pilih',
            command=lambda: self.load_audio_file(),
        )
        pick_cv_button.grid(row=2, column=0, sticky=tk.W)
        preview_cv_button = tk.Button(
            master=ca_dialog_frame,
            text='Buka Audio',
            command= lambda: self.play_audio(),
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

    def load_audio_file(self):
        self.cover_file_dir.set(tkfd.askopenfilename(filetypes=(
            (".WAV Audio", "*.wav"),
        )))
        self.is_mono = (alsb_api.check_is_mono(self.cover_file_dir.get()) == 1)
        if (self.is_mono):
            self.rand_options['Random Byte'].set(0)
            self.options_buttons['Random Byte'].config(state=tk.DISABLED)
        else:
            self.rand_options['Random Byte'].set(0)
            self.options_buttons['Random Byte'].config(state=tk.NORMAL)

    def load_secret_message(self):
        self.secret_message_dir.set(tkfd.askopenfilename())

    def play_audio(self):
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
        self.options_frame.grid(row=self.OPTIONS_ROW, column=0, sticky=tk.W+tk.E)
        row_offset = 0
        for label, mode in self.LSB_MODES:
            self.options_buttons[label] = tk.Radiobutton(
                master=self.options_frame,
                text=label,
                variable=self.lsb_bit_mode,
                value=mode
            )
            self.options_buttons[label].grid(row=row_offset, column=0, sticky=tk.W)
            row_offset += 1
        
        row_offset = 0
        for label in self.RANDOM_OPTIONS:
            if label not in self.rand_options:
                self.rand_options[label] = tk.IntVar()
            self.options_buttons[label] = tk.Checkbutton(
                master=self.options_frame,
                text=label,
                variable=self.rand_options[label]
            )
            self.options_buttons[label].grid(row=row_offset, column=1, sticky=tk.W)
            row_offset += 1
        self.options_buttons['Encrypt'] = tk.Checkbutton(
            master=self.options_frame,
            text='Encrypt message',
            variable=self.use_encryption
        )
        self.options_buttons['Encrypt'].grid(row=row_offset, column=1, sticky=tk.W)

    def execute(self, master, key, output_filename):
        # result = {
        #     'result' : 'debug',
        #     'output_dir' : '/home/fariz/Documents/kuliah/semester8/kripto/tubes1/Yamaha-V50-Rock-Beat-120bpm.wav',
        # }
        if self.cover_file_dir.get() == '' or self.secret_message_dir.get() == '' or key == '' or output_filename == '':
            return

        result = alsb_api.hide_message(
            self.cover_file_dir.get(),
            self.secret_message_dir.get(),
            key,
            output_filename,
            self.rand_options['Random Byte'].get(),
            self.rand_options['Random Frame'].get(),
            self.lsb_bit_mode.get(),
            self.use_encryption.get()
        )
        print('Insertion Finished!')
        master.open_hide_audio_result(result)
        
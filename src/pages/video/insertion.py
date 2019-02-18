import os
import time

import src.steganography.video.lsb as vlsb
import src.steganography.audio.lsb.tools as tools
import tkinter as tk
import tkinter.filedialog as tkfd
import vlc

import src.utilities.ext_vigenere as vig_cipher
import src.utilities.cipher_utils as vig_utils

class VideoInsertionForm(tk.Frame):
    def __init__(self, master):
        self.DEFAULT_OUT_FILENAME = 'video_insertion_result'
        tk.Frame.__init__(self, master)
        self.LSB_MODES = [
            ('1 bit', 1),
            ('2 bit', 2),
        ]
        self.RANDOM_OPTIONS = [
            ('Random Pixel'),
            ('Random Frame'),
        ]
        self.TITLE_ROW = 0
        self.COVER_FILE_ROW = 1
        self.SECRET_MESSAGE_ROW = 2
        self.KEY_ENTRY_ROW = 3
        self.OPTIONS_ROW = 4
        self.SAVEAS_ROW = 5
        self.EXECUTE_ROW = 6

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
        self.lsb_mode = tk.IntVar()
        self.lsb_mode.set(1)
        self.rand_options = {}
        for mode in self.RANDOM_OPTIONS:
            self.rand_options[mode] = tk.IntVar()
            self.rand_options[mode].set(0)
        self.is_encrypt = tk.IntVar()
        self.is_encrypt.set(0)
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
        tk.Label(master=saveas_dialog_frame, text='.avi').grid(row=1, column=1, sticky=tk.W)

        # Tombol Eksekusi dan kembali
        execute_button = tk.Button(self, text='Eksekusi', command=lambda: self.execute(master, key_entry.get(), saveas_entry.get()))
        execute_button.grid(row=self.EXECUTE_ROW, column=0)
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.EXECUTE_ROW, column=1)
    
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
            if label not in self.rand_options:
                self.rand_options[label] = tk.IntVar()
            b = tk.Checkbutton(
                master=options_frame,
                text=label,
                variable=self.rand_options[label]
            )
            b.grid(row=row_offset, column=1, sticky=tk.W)
            row_offset += 1
        
        b = tk.Checkbutton(
            master=options_frame,
            text='Encrypt secret message',
            variable=self.is_encrypt,
        )
        b.grid(row=row_offset, column=1, sticky=tk.W)
        row_offset += 1

    def execute(self, master, key, output_filename):
        # result = {
        #     'result' : 'debug',
        #     'output_dir' : '/home/fariz/Documents/kuliah/semester8/kripto/tubes1/flame.avi',
        # }
        if self.cover_file_dir == '' or self.secret_message_dir == '' or key == '' or output_filename == '':
            return

        print('--- Executing Video LSB Insertion ---')
        print('Cover file: {}'.format(self.cover_file_dir.get()))
        print('Secret file: {}'.format(self.secret_message_dir.get()))
        print('LSB mode: {} bit'.format(self.lsb_mode.get()))
        print('Random Pixel: {}'.format(self.rand_options['Random Pixel'].get()))
        print('Random Frame: {}'.format(self.rand_options['Random Frame'].get()))
        print('Encrypt Message: {}'.format(self.is_encrypt.get()))

        temp_file_name = 'vid_enc_temp'
        if (self.is_encrypt.get()):
            has_extension = self.secret_message_dir.get().split('/')[-1].find('.') != -1
            if has_extension:
                temp_file_name += '.' + self.secret_message_dir.get().split('.')[-1]
            msg_plain_text = vig_utils.read_input_bytes(self.secret_message_dir.get())
            encryptor = vig_cipher.ExtendedVigenere()
            cipher_text = encryptor.encipher(msg_plain_text, key)
            vig_utils.save_output_bytes(cipher_text, temp_file_name)

        result = vlsb.hide_secret(
            self.cover_file_dir.get(),
            (self.secret_message_dir.get() if not self.is_encrypt.get() else temp_file_name),
            key,
            (output_filename + '.avi'),
            self.lsb_mode.get(),
            is_seq_frame=not(self.rand_options['Random Frame'].get()),
            is_seq_pixel=not(self.rand_options['Random Pixel'].get()),
            is_encrypted=self.is_encrypt.get()
        )
        # if (self.is_encrypt.get()):
        #     os.remove(temp_file_name)
        print('Insertion finished!')
        master.open_hide_video_result(result)
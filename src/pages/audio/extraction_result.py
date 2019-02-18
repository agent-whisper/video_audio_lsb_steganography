import time

import tkinter as tk
import vlc

class AudioExtractionResult(tk.Frame):
    def __init__(self, master, output_result={'result':'failed'}):
        tk.Frame.__init__(self, master)
        self.TITLE_ROW = 0
        self.RESULT_ROW = 1
        # Judul halaman
        tk.Label(self, text='Hasil Ekstraksi Audio', font='none 24 bold').grid(row=self.TITLE_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)

        # Output dan playback
        self.render_result_frame(output_result)

        # Tombol Eksekusi dan kembali
        return_button = tk.Button(self, text='Kembali', command=lambda: master.open_main_menu())
        return_button.grid(row=self.RESULT_ROW+1, column=0, columnspan=2)

    def render_result_frame(self, output_result):
        rr_frame = tk.Frame(self)
        rr_frame.grid(row=self.RESULT_ROW, column=0, columnspan=2, sticky=tk.W+tk.E)
        try:
            if output_result['result'] == 'failed':
                tk.Label(master=rr_frame, text='Ekstraksi gagal [result:{}]'.format(output_result['result'])).grid(row=0, column=0)
            else:
                tk.Label(master=rr_frame, text='Ekstraksi berhasil [result:{}]'.format(output_result['result'])).grid(row=0, column=0, columnspan=2, sticky=tk.W)
                tk.Label(master=rr_frame, text='Lokasi output:').grid(row=1, column=0, sticky=tk.W)
                tk.Label(master=rr_frame, text=output_result['output_dir']).grid(row=1, column=1, sticky=tk.W)
        except KeyError as e:
            tk.Label(master=rr_frame, text='Output Result Key Error!').grid(row=0, column=0)
            print(e)
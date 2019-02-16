import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.place(relx=0.5, rely=0.1, y=48, anchor=tk.CENTER)

        tk.Label(self, text='Tugas Besar 1', font='none 24 bold').grid(row=0, columnspan=2, sticky=tk.W+tk.E)

        ins_vid_button = tk.Button(self, text='Sembunyikan Pesan ke Video')
        ext_vid_button = tk.Button(self, text='Ekstrak Pesan dari Video')
        ins_vid_button.grid(row=1, column=0, sticky=tk.W)
        ext_vid_button.grid(row=1, column=1, sticky=tk.W)

        ins_aud_button = tk.Button(self, text='Sembunyikan Pesan ke Audio')
        ext_aud_button = tk.Button(self, text='Ekstrak Pesan dari Audio')
        ins_aud_button.grid(row=2, column=0, sticky=tk.W)
        ext_aud_button.grid(row=2, column=1, sticky=tk.W)

        exit_button = tk.Button(self, text='Keluar', command=master.destroy)
        exit_button.grid(row=3, column=0, columnspan=2)
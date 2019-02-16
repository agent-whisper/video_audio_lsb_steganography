#!/usr/bin/python3
import tkinter as tk
from app.gui import App

mw = App(title='Tugas Besar 1')
# mw.title('Tugas Besar 1')
# window_width='500'
# window_height='300'
# mw.geometry('{}x{}'.format(window_width,window_height))
# # mw.resizable(0, 0)

# main_menu = tk.Frame(master=mw)
# main_menu.place(relx=0.5, rely=0.1, y=48, anchor=tk.CENTER)

# tk.Label(master=main_menu, text='Tugas Besar 1', font='none 24 bold').grid(row=0, columnspan=2, sticky=tk.W+tk.E)

# ins_vid_button = tk.Button(master=main_menu, text='Sembunyikan Pesan ke Video')
# ext_vid_button = tk.Button(master=main_menu, text='Ekstrak Pesan dari Video')
# ins_vid_button.grid(row=1, column=0, sticky=tk.W)
# ext_vid_button.grid(row=1, column=1, sticky=tk.W)

# ins_aud_button = tk.Button(master=main_menu, text='Sembunyikan Pesan ke Audio')
# ext_aud_button = tk.Button(master=main_menu, text='Ekstrak Pesan dari Audio')
# ins_aud_button.grid(row=2, column=0, sticky=tk.W)
# ext_aud_button.grid(row=2, column=1, sticky=tk.W)

# exit_button = tk.Button(master=main_menu, text='Keluar', command=mw.destroy)
# exit_button.grid(row=3, column=0, columnspan=2)
mw.mainloop()

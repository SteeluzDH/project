import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import sounddevice as sd
import wavio as wv
from scipy.io.wavfile import write


# Window
window = tk.Tk()
window.title('Mood Sensor')
window.geometry('800x360')
window.configure(bg='#5696b8')

# Toolbar menu
tb_menu = tk.Menu(window)

# tb_submenu
file_menu = tk.Menu(tb_menu, tearoff=False)
file_menu.add_command(label='New file', command=lambda: print('New file'))
file_menu.add_command(label='Open file', command=lambda: print('Open file'))
tb_menu.add_cascade(label='File', menu=file_menu)

# second tb_submenu
about_menu = tk.Menu(tb_menu, tearoff=False)
about_menu.add_command(label='About Us', command=lambda: print('This project was created by \nDavid Norman. \nMing Fondberg. \nMuhannad Naser. \nParsan Amani '))
tb_menu.add_cascade(label='About', menu=about_menu)

window.configure(menu=tb_menu)


# main frame title
title_label = ttk.Label(master=window,
                        text='Mood Sensor',
                        background='#5696b8',
                        foreground='black')
title_label.pack()


# output frame
output_frame = ttk.Frame(master=window)
output_label = ttk.Label(master=output_frame,
                         background='#5696b8',
                         text='displays the current mood')
output_label.pack()
output_frame.pack()

# input frame
input_frame = ttk.Frame(master=window)
input_entry = ttk.Entry(master=input_frame)
input_button = ttk.Button(master=input_frame, text='test', command=lambda: print('test button'))

input_entry.pack()
input_button.pack()
input_frame.pack()

window.mainloop()
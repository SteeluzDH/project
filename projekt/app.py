
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import sounddevice as sd
import wavio as wv
from scipy.io.wavfile import write



mood = 0

# function for color change
def colorchange ():
    global mood
    if mood > 3:
        mood = 0

    mood += 1
    if mood == 1:
        window.configure(bg='green')
    
    elif mood == 2:
        window.configure(bg='red')
    
    elif mood == 3:
        window.configure(bg='blue')
    
    else:
        window.configure(bg='#5696b8')

# function to record audio
def record():
    # Sampling freq
    freq = 44100
    
    # Rec Duration
    duration = 5
    
    # Start the recorder with given values of duration and frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    
    # Record audio for the giving number of seconds
    sd.wait()
    
    # convert the numpy array to an audio file with the given sampling frequency
    write("recording0.wav", freq, recording)
    
    # convert the numpy array to an audio file.
    wv.write("recording1.wav", recording, freq, sampwidth=2)
    

# initialise app-window
# main window
window = tk.Tk()
window.title('Demo')
window.geometry('360x800')
window.configure(bg='#5696b8')


# menu
menu = tk.Menu(window)

# sub-menu
file_menu = tk.Menu(menu, tearoff=False)
file_menu.add_command(label="New", command=lambda: print('New file'))
file_menu.add_command(label="Open", command=lambda: print('Open file'))
menu.add_cascade(label='File', menu=file_menu)

# another sub-menu
about_menu = tk.Menu(menu, tearoff=False)
about_menu.add_command(label="About us", command=lambda: print('This project was created by \nDavid Norman. \nMing Fondberg. \nMuhannad Naser. \nParsan Amani '))
menu.add_cascade(label="About", menu=about_menu)

window.configure(menu=menu)


# title
title_lable = ttk.Label(master=window,
                        text='Emotion detection',
                        font='Calibri 24',
                        background='#5696b8',
                        foreground='black')
title_lable.pack()

# importing special button-image
#rec_button = PhotoImage('record-icon.jpg', height=75, width=75)

# output field
output_frame = ttk.Frame(master=window)
output_window = tk.Text(master=output_frame, background='#1d4b63')

output_window.pack()
output_frame.pack()

# input field
input_frame = ttk.Frame(master=window)

#button = ttk.Button(master=input_frame, image='record-icon.jpg')
mood_btn = ttk.Button(master=input_frame, text='cycle', command=colorchange)
button = ttk.Button(master=input_frame, text='record', underline=False, command=record)
mood_btn.pack(side='left')
button.pack(side='left')
input_frame.pack(pady=10, anchor='center', expand=True)


# color change


# mainloop
window.mainloop()


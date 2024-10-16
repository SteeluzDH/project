
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import sounddevice as sd
import wavio as wv
from scipy.io.wavfile import write
import pipeline
import webbrowser


mood = "neutral"
# function for color change #not necessery only if wanted
def colorchange ():
    global mood
    if mood == "happy":
        window.configure(bg='#0c8b45')
    
    elif mood == "sad":
        window.configure(bg='#ff3000')
    
    elif mood == "angry":
        window.configure(bg='#000e80')
    
    else:
        window.configure(bg='#818181')

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
    
def open_spotify():
    webbrowser.open_new_tab("https://open.spotify.com/genre/section0JQ5DACFo5h0jxzOyHOsIc")
    

# initialise app-window
# main window
window = tk.Tk()
window.title('Demo')
window.geometry('360x800')
window.configure(bg='#818181')
icon = PhotoImage(file="./ds.png")
window.iconphoto(False, icon)

# menu
menu = tk.Menu(window)

# sub-menu
link_menu = tk.Menu(menu, tearoff=False)
link_menu.add_command(label="Link Spotify", command=lambda: webbrowser.open("https://www.spotify.com/account/overview/")) # open seperate window for spotify credentials.
link_menu.add_command(label="Open Spotify", command=lambda: webbrowser.open_new_tab("https://open.spotify.com/genre/section0JQ5DACFo5h0jxzOyHOsIc"))
menu.add_cascade(label='Link', menu=link_menu)

# another sub-menu
about_menu = tk.Menu(menu, tearoff=False)
about_menu.add_command(label='About Us', command=lambda: print('This project was created by '
                                                               '\nDavid Norman.'
                                                               '\nMing Fondberg.' 
                                                               '\nMuhannad Naser.' 
                                                               '\nParsan Amani '))
menu.add_cascade(label="About", menu=about_menu)

window.configure(menu=menu)

# title
title_lable = ttk.Label(master=window,
                        text='Emotion detection',
                        font='Calibri 24',
                        background='#818181',
                        foreground='black')
title_lable.pack()


# output field
output_frame = ttk.Frame(master=window)

# output widgets
output_window = tk.Text(master=output_frame, background='#818181')
output_window.pack()
output_frame.pack()

# input field
input_frame = ttk.Frame(master=window)

# input widgets
mood_btn = ttk.Button(master=input_frame, text='cycle', command=colorchange)
button = ttk.Button(master=input_frame, text='record', underline=False, command=record)
mood_btn.pack(side='left')
button.pack(side='left')
input_frame.pack(pady=10, anchor='center', expand=True)


# mainloop
window.mainloop()


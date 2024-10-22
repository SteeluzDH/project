import tkinter as tk
import customtkinter as ctk
from tkinter import PhotoImage
import sounddevice as sd
from scipy.io.wavfile import write
import pipeline
import wavio as wv
import owntest
import os
import webbrowser

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # turns of information, still shows errors

# function to record audio
def record():
    text_output.insert(ctk.END, 'Recording and analyzing voice...\n')
    # Sampling freq
    freq = 44100
    
    # Rec Duration
    duration = 4
    
    # Start the recorder with given values of duration and frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    
    # Record audio for the giving number of seconds
    sd.wait()
    
    # convert the numpy array to an audio file with the given sampling frequency
    write("recording0.wav", freq, recording)
    
    # convert the numpy array to an audio file.
    wv.write("recording1.wav", recording, freq, sampwidth=2)
    
    # calls on analyze
    owntest.record_and_analyse()
    text_output.insert(ctk.END, owntest.record_and_analyse)

def start_spotify():
    text_output.insert(ctk.END, "Starting Spotify...\n")
    webbrowser.open_new_tab("https://open.spotify.com")

def about():
    text_output.insert(ctk.END, 'This project was created by '
                       '\nDavid Norman.'
                       '\nMing Fondberg.'
                       '\nMuhannad Naser.'
                       '\nParsan Amani ' )

window = ctk.CTk()
window.title("Emotion Detector")
window.geometry('400x800')
window.configure()
W_icon = PhotoImage(file="ds.png")
window.iconphoto(False, W_icon)
# menu
menu = tk.Menu(window)

# sub-menu
link_menu = tk.Menu(menu, tearoff=False)
link_menu.add_command(label="Link Spotify", command=lambda: webbrowser.open("https://www.spotify.com/account/overview/")) # open seperate window for spotify credentials.
link_menu.add_command(label="Open Spotify", command=lambda: webbrowser.open_new_tab("https://open.spotify.com/genre/section0JQ5DACFo5h0jxzOyHOsIc"))
menu.add_cascade(label='Link', menu=link_menu)

# another sub-menu
about_menu = tk.Menu(menu, tearoff=False)
about_menu.add_command(label='About Us', command=about)
menu.add_cascade(label="About", menu=about_menu)

window.configure(menu=menu)

# title widget
title_lbl = ctk.CTkLabel(window, text="Emotion Detection",
                         font=('Calibri', 24))
title_lbl.place(relx=0.25, rely=0.1)

# text output widget
text_output = ctk.CTkTextbox(window)
text_output.place(relx=0.25, rely=0.2)

# button widgets
spotify_btn = ctk.CTkButton(window, text='Spotify', command=start_spotify, corner_radius=50)
record_btn = ctk.CTkButton(window, text="Record and analyze", command=record, corner_radius=50)


spotify_btn.place(relx=0.01, rely=0.9, relheight=0.05 )
record_btn.place(relx=0.41, rely=0.9, relheight=0.05)

window.mainloop()
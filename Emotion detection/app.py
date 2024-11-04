from customtkinter import *
from tkinter import filedialog
import sounddevice as sd
from scipy.io.wavfile import write
import pipeline
import wavio as wv
import owntest
import os
import webbrowser
import audio_analysis
from time import strftime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # turns of information, still shows errors
audio_file_path = "kidstalkingbythedoor.wav"

# function to record audio
def record():
    # changing button color to red when pressed
    record_btn.configure(fg_color="red")
    text_output.insert(END, 'Recording and analyzing voice...\n')
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
    owntest.record_and_analyse(text_output)
    
    # reverting to original color
    record_btn.configure(fg_color="#2E8B57")  # Replace with your original button color

# creating open file func
def open_file():
    global audio_file_path, analyzer  # global variable updates
    file = filedialog.askopenfile(mode='r', filetypes=[('Audio files', '*.wav')])
    if file:
        audio_file_path = os.path.abspath(file.name)  # updates filepath
        text_output.insert(END, f'File selected: {audio_file_path}\n')
        
        # Updates analyzer object with new filepath
        analyzer = audio_analysis.AudioAnalyzer(audio_file_path, text_output=text_output)

# creating start spotify func
def start_spotify():
    text_output.insert(END, "Starting Spotify...\n")
    webbrowser.open_new_tab("https://open.spotify.com")

# creating about func
def about():
    text_output.insert(END, 'This project was created by '
                       '\nDavid Norman.'
                       '\nMing Fondberg.'
                       '\nMuhannad Naser.'
                       '\nParsan Amani ' )

# creating clock func
def clock():
    string = strftime('%H:%M:%S %p')
    lbl.configure(text=string)
    lbl.after(1000, clock)

# creating clear func 
def cls():
    text_output.delete('1.0', 'end' )


# creating main window.
main_window = CTk()
main_window.title('Emotion Detection')
main_window.geometry('500x800')
main_window.configure()

# clock widget
lbl = CTkLabel(main_window, font=('oswald', 16, 'bold'), text_color='green')
lbl.place(relx=0.01, rely=0.01 )
clock()

# text output
text_output = CTkTextbox(master=main_window, fg_color='black', text_color='green', font=('oswald', 14))
text_output.place(relx=0.0, rely=0.04, relwidth=1, relheight=0.6)

# button widgets
spotify_btn = CTkButton(master=main_window, text='spotify', command=start_spotify)
enter_btn = CTkButton(master=main_window, text='Enter')
about_btn = CTkButton(master=main_window, text='About', command=about)

analys_btn = CTkButton(master=main_window, text='Analyse audio', command=lambda: analyzer.compute_features())
record_btn = CTkButton(master=main_window, text='Record', command=record, fg_color="#2E8B57")
select_btn = CTkButton(master=main_window, text='Select file', command=open_file)

cls_btn = CTkButton(master=main_window, text='cls', command=cls)
plot_btn = CTkButton(master=main_window, text='Plot waveform', command=lambda: analyzer.plot_waveform())
plotF_btn = CTkButton(master=main_window, text='Plot features', command=lambda: analyzer.plot_features())

# placing widgets
spotify_btn.place(relx=0.01, rely=0.9)
enter_btn.place(relx=0.31, rely=0.9)
about_btn.place(relx=0.61, rely=0.9)

cls_btn.place(relx=0.01, rely=0.85)
record_btn.place(relx=0.31, rely=0.85)
select_btn.place(relx=0.61, rely=0.85)

analys_btn.place(relx=0.01, rely=0.8)
plotF_btn.place(relx=0.31, rely=0.8)
plot_btn.place(relx=0.61, rely=0.8)


main_window.mainloop()
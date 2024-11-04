from customtkinter import *
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
    
    ''' # calls on analyze
    owntest.record_and_analyse()
    text_output.insert(END, owntest.record_and_analyse)'''

def open_file():
    global audio_file_path
    file = filedialog.askopenfile(mode='r', filetypes=[('Audio files', '*.wav')])
    if file:
        filepath = os.path.abspath(file.name)
        audio_file_path = file
        text_output.insert(END, f'File selected: {filepath}\n')

def start_spotify():
    text_output.insert(END, "Starting Spotify...\n")
    webbrowser.open_new_tab("https://open.spotify.com")

def about():
    text_output.insert(END, 'This project was created by '
                       '\nDavid Norman.'
                       '\nMing Fondberg.'
                       '\nMuhannad Naser.'
                       '\nParsan Amani ' )

def clock():
    string = strftime('%H:%M:%S %p')
    lbl.configure(text=string)
    lbl.after(1000, clock)
 
# clear textbox func
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

analyzer = audio_analysis.AudioAnalyzer(audio_file_path, text_output=text_output)

# button widgets
left_btn = CTkButton(master=main_window, text='<-')
enter_btn = CTkButton(master=main_window, text='Enter')
right_btn = CTkButton(master=main_window, text='->')

analys_btn = CTkButton(master=main_window, text='Analyse audio', command=analyzer.compute_features)
record_btn = CTkButton(master=main_window, text='Record', command=record)
select_btn = CTkButton(master=main_window, text='Select file', command=open_file)

cls_btn = CTkButton(master=main_window, text='cls', command=cls)
plot_btn = CTkButton(master=main_window, text='Plot waveform', command=analyzer.plot_waveform)
plotF_btn = CTkButton(master=main_window, text='Plot features', command=analyzer.plot_features)


# placing widgets
left_btn.place(relx=0.01, rely=0.9)
enter_btn.place(relx=0.31, rely=0.9)
right_btn.place(relx=0.61, rely=0.9)

cls_btn.place(relx=0.01, rely=0.85)
record_btn.place(relx=0.31, rely=0.85)
select_btn.place(relx=0.61, rely=0.85)

analys_btn.place(relx=0.01, rely=0.8)
plotF_btn.place(relx=0.31, rely=0.8)
plot_btn.place(relx=0.61, rely=0.8)


main_window.mainloop()
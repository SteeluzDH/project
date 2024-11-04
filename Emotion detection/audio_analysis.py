from customtkinter import *
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

class AudioAnalyzer:
    def __init__(self, audio_file_path, text_output=None):
        """
        Initialize the AudioAnalyzer class.
        
        Parameters:
            file_path (str): Path to the audio (.wav) file.
            text_output (tkinter.Text or None): Text widget for output display (optional).
        """
        self.file_path = audio_file_path
        self.text_output = text_output
        self.audio_data, self.sample_rate = librosa.load(audio_file_path, sr=None)

    def compute_features(self):
        """
        Compute basic audio features for EDA.
        
        Returns:
            dict: Contains RMS energy, zero-crossing rate, and spectral centroid.
        """
        rms_energy = librosa.feature.rms(y=self.audio_data)[0]
        zero_crossings = librosa.zero_crossings(self.audio_data, pad=False)
        zcr = np.sum(zero_crossings)
        spectral_centroid = librosa.feature.spectral_centroid(y=self.audio_data, sr=self.sample_rate)[0]

        self.features = {
            "rms_energy": rms_energy,
            "zero_crossing_rate": zcr,
            "spectral_centroid": spectral_centroid
        }
        file_name = os.path.basename(self.file_path)
        if self.text_output:
            self.text_output.insert(END, f"Audio Name: {file_name}\n")
            self.text_output.insert(END, f"Audio Duration (s): {len(self.audio_data) / self.sample_rate}\n")
            self.text_output.insert(END, f"Audio Data Shape: {self.audio_data.shape}\n")
            self.text_output.insert(END, f"Sample Rate: {self.sample_rate}\n")
            self.text_output.insert(END, f"RMS Energy Shape: {rms_energy.shape}\n")
            self.text_output.insert(END, f"Zero Crossing Rate: {zcr}\n")
            self.text_output.insert(END, f"Spectral Centroid Shape: {spectral_centroid.shape}\n")


        else:
            print("Sample Rate:", self.sample_rate)
            print("Audio Duration (s):", len(self.audio_data) / self.sample_rate)
            print("Audio Data Shape:", self.audio_data.shape)
            print("RMS Energy Shape:", rms_energy.shape)
            print("Zero Crossing Rate:", zcr)
            print("Spectral Centroid Shape:", spectral_centroid.shape)

        return self.features



    def plot_waveform(self):
        plt.figure(figsize=(15, 5))
        librosa.display.waveshow(self.audio_data, sr=self.sample_rate)
        plt.title('Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()

    def plot_features(self):
        if not hasattr(self, 'features'):
            self.compute_features()

        rms_energy = self.features['rms_energy']
        spectral_centroid = self.features['spectral_centroid']

        plt.figure(figsize=(15, 10))
        plt.subplot(2, 1, 1)
        plt.plot(rms_energy, color='purple')
        plt.title('RMS Energy')
        plt.xlabel('Frames')
        plt.ylabel('Energy')

        plt.subplot(2, 1, 2)
        frames = range(len(spectral_centroid))
        time = librosa.frames_to_time(frames, sr=self.sample_rate)
        plt.plot(time, spectral_centroid, color='green')
        plt.title('Spectral Centroid')
        plt.xlabel('Time (s)')
        plt.ylabel('Hz')

        plt.tight_layout()
        plt.show()

import tensorflow as tf
from tensorflow.keras.models import load_model
from customtkinter import *
import librosa
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Stänger av information och varningar, men visar fel

# Load the saved model
model = load_model('./final_model.keras')

# Load the original labels used during training
y = np.load('y_labels.npy')

# Encode the labels using LabelEncoder (just as in training)
le = LabelEncoder()
y_encoded = le.fit_transform(y)  # Fit the encoder with the original labels

# Function to extract MFCC features from a new audio file
def extract_mfcc(file_path, n_mfcc=13, max_pad_len=100):
    audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast')  # Load audio
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)   # Extract MFCC features
    
    # Check if the MFCC's number of columns is less than max_pad_len
    if mfcc.shape[1] < max_pad_len:
        pad_width = max_pad_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')  # Pad MFCCs
    else:
        # If it's longer, truncate the MFCC features
        mfcc = mfcc[:, :max_pad_len]
    
    return mfcc

def record_and_analyse(text_output):
    text_output=text_output
    # Example path to the test audio file
    test_mfcc = extract_mfcc('./recording1.wav')
    test_mfcc = test_mfcc.reshape(1, 100, 13)  # Reshape to fit the model input shape

    # Make a prediction
    prediction = model.predict(test_mfcc)
    predicted_class = np.argmax(prediction)  # Get the predicted class (e.g., emotion label)

    # Get the corresponding original label
    predicted_emotion = le.inverse_transform([predicted_class])
    text_output.insert(END,f"Predicted emotion: {predicted_emotion[0]}")
    if __name__ == "__main__":
        record_and_analyse()
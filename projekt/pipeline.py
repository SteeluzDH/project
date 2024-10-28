import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fastapi import FastAPI, File, UploadFile
import librosa
import tensorflow as tf
import numpy as np

# Spotify API credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id='6010233a66504798a679459effe9fc88',
    client_secret='b58d958ad39e4c7fb5cf3634da35ce84'
))

# Initiera FastAPI och ladda modellen
app = FastAPI()
model = tf.keras.models.load_model("./final_model.keras")  

# Root endpoint för att testa servern
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is working!"}

# Funktion för att returnera en playlist baserat på humör
def get_playlist_for_mood(mood: str):
    playlists = {
        "calm": "https://open.spotify.com/playlist/7sidFnkAuX6i59Ng7Z8zWZ?si=13938932183f4c3d",
        "energetic": "https://open.spotify.com/playlist/2JzBPsjlH6fkNdYNPUzz6G?si=d77af8fb74624cda",
        "happy": "https://open.spotify.com/playlist/6wymJv4f1ukGcNabS0tsXf?si=dffe1d0950324c54",
        "angry": "https://open.spotify.com/playlist/0e12Inp4tMgV2HkXkQp3xX?si=32aa7323357c436f",
        "surprised": "https://open.spotify.com/playlist/37i9dQZF1EfZiV3tQEnHwW?si=4276df1456374277"
    }
    return playlists.get(mood, "spotify:playlist:YOUR_DEFAULT_PLAYLIST_URI")

# Funktion för att förutsäga humör från ljuddata
def predict_mood(audio_data):
    # Förbearbeta ljuddata för modellen
    mfcc = librosa.feature.mfcc(y=audio_data, sr=22050, n_mfcc=40)
    mfcc_scaled = np.mean(mfcc.T, axis=0)
    
    # Gör prediktionen
    mfcc_scaled = np.expand_dims(mfcc_scaled, axis=0)  # Lägg till batch dimension
    prediction = model.predict(mfcc_scaled)
    mood_index = np.argmax(prediction)  # Få index för högsta sannolikhet
    mood_map = {0: "calm", 1: "energetic", 2: "happy"}  # Anpassa efter din modell
    return mood_map.get(mood_index, "unknown")

# Endpoint för att analysera röstfil
@app.post("/analyze-voice/")
async def analyze_voice(file: UploadFile = File(...)):
    audio_data, sr = librosa.load(file.file, sr=22050)
    
    # Förutsäg humöret med hjälp av modellen
    mood = predict_mood(audio_data)
    
    # Hämta tillhörande Spotify playlist
    playlist = get_playlist_for_mood(mood)
    
    return {
        "mood": mood,
        "playlist": playlist,
        "message": "Voice analyzed successfully!"
    }
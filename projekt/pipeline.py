import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fastapi import FastAPI, File, UploadFile
import librosa  # Ensure this is installed for audio processing

# Spotify API credentials
def link_spotify():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id='6010233a66504798a679459effe9fc88',  # Replace with your actual client ID
        client_secret='b58d958ad39e4c7fb5cf3634da35ce84'  # Replace with your actual client secret
    ))

app = FastAPI()

# Root endpoint to test the server is running
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is working!"}

# Function to return a playlist based on mooduvicorn main:app --reload
def get_playlist_for_mood(mood: str):
    # Mapping moods to specific Spotify playlists
    playlists = {
        "calm": "spotify:playlist:YOUR_CALM_PLAYLIST_URI",  # Replace with your actual calm playlist URI
        "energetic": "spotify:playlist:YOUR_ENERGETIC_PLAYLIST_URI",  # Replace with your actual energetic playlist URI
        "happy": "spotify:playlist:YOUR_HAPPY_PLAYLIST_URI",  # Replace with your actual happy playlist URI
        "neutral": "spotify:playlist:YOUR_HAPPY_PLAYLIST_URI",  # Replace with your actual happy playlist URI - # neutral plays random playlists
    }
    # Return the corresponding playlist for the detected mood, or a default if none match
    return playlists.get(mood, "spotify:playlist:YOUR_DEFAULT_PLAYLIST_URI")  # Default playlist URI

# Endpoint to upload and analyze voice file
@app.post("/analyze-voice/")
async def analyze_voice(file: UploadFile = File(...)):
    # Load the audio file using librosa
    audio_data, sr = librosa.load(file.file, sr=None)
    
    # Placeholder for mood detection (you can implement your logic here)
    mood = "calm"  # For now, assume every file leads to a "calm" mood
    
    # Get the corresponding playlist based on the detected mood
    playlist = get_playlist_for_mood(mood)
    
    return {
        "mood": mood,
        "playlist": playlist,
        "message": "Voice analyzed successfully!"
    }
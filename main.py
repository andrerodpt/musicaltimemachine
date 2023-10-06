import requests
from bs4 import BeautifulSoup
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from credentials import SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

BILLBOARD_BASE_URL = 'https://www.billboard.com/charts/hot-100/'

response = requests.get(f"{BILLBOARD_BASE_URL}{date}")
response.raise_for_status()
billboard_html = response.text

def scrape_data(billboard_html):
    soup = BeautifulSoup(billboard_html, 'html.parser')
    songs = soup.select(".chart-results-list li h3")
    songs_list = []
    for song in songs:
        songs_list.append(song.text.strip())
    return songs_list

def create_playlist(user_id):
    playlist = sp.user_playlist_create(
        user=user_id, 
        name=f"{date} Billboard 100", 
        public=False, 
        collaborative=False, 
        description=f"This is a playlist created with the top 100 songs from Billboard for the day {date}"
    )
    return playlist

songs_list = scrape_data(billboard_html)

# Creating the Spotipy Object
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,  # Your URI
        client_id=SPOTIPY_CLIENT_ID,  # YOUR CLIENT ID
        client_secret=SPOTIPY_CLIENT_SECRET,  # Your Client Secret
        show_dialog=True,
        cache_path="token.txt"
    )
)

# Get the user id 
user_id = sp.current_user()["id"]

# Create the playlist
playlist = create_playlist(user_id)

# Get the song uri from Spotify
tracks_uris = []
for song in songs_list:
    query = f"track: {song} year: {date[:4]}"
    music_search_results = sp.search(q=query, limit=1, offset=0, type='track', market=None)
    if len(music_search_results['tracks']['items']) > 0:
        song_uri = music_search_results['tracks']['items'][0]['uri']
        tracks_uris.append(song_uri)

# Add songs to previously created playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_uris)
    
    
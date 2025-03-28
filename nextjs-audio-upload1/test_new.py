import requests
from dotenv import load_dotenv
import os
import urllib.parse
import webbrowser
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import shutil
import time
import yt_dlp
from youtubesearchpython import VideosSearch

load_dotenv()

audio_folder = r"C:\Users\bhave\Documents\Epoch 2.0\nextjs-audio-upload1\public\uploads"
os.makedirs(audio_folder, exist_ok=True)

# Delete existing files in the directory
for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)  # Delete the file
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Replace these with your actual Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URL")
API_URL = "https://api.spotify.com/v1"
# Spotify API endpoints
# Scopes required for accessing user data
SCOPES = "user-library-read user-read-recently-played user-top-read"

def get_liked_songs(token):
    headers = {"Authorization": f"Bearer {token}"}
    liked_songs = []
    url = f"{API_URL}/me/tracks"

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Process each track in the current page of results
        for item in data['items']:
            track_id = item['track']['id']
            liked_songs.append(track_id)
            
        url = data.get("next")  # Get next page URL if it exists

    return liked_songs

def get_most_played_ids(token, limit=10):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/me/top/tracks?limit={limit}&time_range=long_term", headers=headers)

    if response.status_code == 200:
        return [item["id"] for item in response.json()["items"]]
    else:
        raise Exception(f"Failed to get most played tracks: {response.json()}")

def get_recently_played(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/me/player/recently-played?limit=50", headers=headers)

    if response.status_code == 200:
        data = response.json()
        for item in data["items"]:
            print(f"Track: {item['track']['name']}")

        return [item["track"]["id"] for item in response.json()["items"]]
    else:
        raise Exception(f"Failed to get recently played tracks: {response.json()}")
def get_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    playlists = response.json()
    return playlists
def get_playlist_tracks(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    headers = { "Authorization": f"Bearer {token}" }
    response = requests.get(url, headers=headers)
    tracks = response.json()
    return [item["track"]["id"] for item in tracks["items"]]
def get_auth_url():
    """Generate the correct Spotify authorization URL."""
    base_url = "https://accounts.spotify.com/authorize"
    
    # Encode the redirect URI
    encoded_redirect_uri = urllib.parse.quote(REDIRECT_URI, safe="")

    # Encode the scope (spaces should be %20)
    encoded_scope = urllib.parse.quote(SCOPES)

    # Construct the full URL
    auth_url = (
        f"{base_url}?"
        f"client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={encoded_redirect_uri}"
        f"&scope={encoded_scope}"
    )

    return auth_url

def get_access_token(auth_code):
    """Exchange authorization code for access token."""
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(token_url, data=payload)
    token_data = response.json()

    if "access_token" in token_data:
        return token_data["access_token"]
    else:
        print("Error:", token_data)
        return None

def search_youtube(song_name):
    """Search YouTube for the song"""
    search = VideosSearch(song_name, limit=1, language='en', region='US')
    result = search.result()["result"][0]["link"]
    return result

def download_song(youtube_url, track_id):
    """Download song from YouTube as MP3"""
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        "outtmpl": os.path.join(audio_folder, f"{track_id}"),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def download_songs(token):
    ids = get_liked_songs(token)
    #ids = get_most_played_ids(token)
    for i in ids:
        song_name = i
        try:
            youtube_link = search_youtube(song_name)
            download_song(youtube_link, i)
            print(f"Downloaded: {song_name}")
        except IndexError:
            print(f"Could not find YouTube video for: {song_name}")
            continue
        except Exception as e:
            print(f"Error downloading {song_name}: {str(e)}")
            continue

# Create a global event to signal when auth code is received
auth_received = threading.Event()

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract authorization code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        auth_code = params.get('code', [None])[0]
        
        # Set the auth_code in the server instance
        if hasattr(self.server, 'auth_code'):
            self.server.auth_code = auth_code
            # Signal that we've received the auth code
            auth_received.set()
        
        # Send response to browser
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Create HTML response that instructs user to close the window
        message_html = """
        <html>
        <head>
            <title>Spotify Authorization Successful</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h2 { color: #1DB954; margin-bottom: 20px; } /* Spotify green */
                p { line-height: 1.6; margin-bottom: 15px; }
                .success-icon { font-size: 48px; margin-bottom: 20px; color: #1DB954; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success-icon">✓</div>
                <h2>Authorization Successful!</h2>
                <p>Your Spotify authentication is complete.</p>
                <p><strong>You can now close this window and return to the application.</strong></p>
                <p>The download process has started in the background.</p>
            </div>
            <script>
                // Try to close the window (may not work in all browsers)
                try {
                    window.close();
                } catch (e) {
                    console.log("Auto-close not supported by this browser");
                }
            </script>
        </body>
        </html>
        """
        
        self.wfile.write(message_html.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress server logs
        return

def main():
    """Automated process to get Spotify token."""
    print("Starting Spotify authentication process...")
    
    # Create and configure the HTTP server
    server = HTTPServer(('localhost', 8888), CallbackHandler)
    server.auth_code = None
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server started on port 8888")
    
    # Open Spotify authorization page automatically
    auth_url = get_auth_url()
    print("Opening authorization URL in browser...")
    webbrowser.open_new(auth_url)
    
    # Wait for the authorization code with a timeout
    print("Waiting for authorization...")
    
    # Set a timeout of 5 minutes (300 seconds)
    timeout = 300
    
    # Wait for the auth_received event to be set with a timeout
    auth_success = auth_received.wait(timeout)
    
    if not auth_success:
        print("Authentication timed out after 5 minutes")
        server.shutdown()
        return
        
    # Get the authorization code
    auth_code = server.auth_code
    print(f"Authorization code received: {auth_code[:5]}...")
    
    # Shutdown the server (in a separate thread to avoid blocking)
    shutdown_thread = threading.Thread(target=server.shutdown)
    shutdown_thread.daemon = True
    shutdown_thread.start()
    
    if auth_code:
        # Exchange the authorization code for an access token
        access_token = get_access_token(auth_code)
        if access_token:
            print("Access token successfully retrieved!")
            print(f"Token: {access_token[:10]}...")
            
            # Now download the songs
            print("Starting to download songs...")
            download_songs(access_token)
            #print(get_playlist_tracks(access_token, get_playlists(access_token)["items"][0]["id"]))
            print("Process completed!")
        else:
            print("Failed to retrieve access token.")
    else:
        print("Could not extract authorization code from the URL.")

if __name__ == "__main__":
    main()
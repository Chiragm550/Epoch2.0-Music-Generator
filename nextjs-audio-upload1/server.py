from flask import Flask, request, jsonify, send_file
import os
import shutil
import subprocess
import threading
import pandas as pd
from orchestrator import graph
import asyncio



app = Flask(__name__)

from flask_cors import CORS
CORS(app)

UPLOAD_FOLDER = "public/uploads"

def clear_upload_folder():
    """Deletes all files in the upload folder."""
    if os.path.exists(UPLOAD_FOLDER):
        for file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file)
            os.remove(file_path)

@app.route("/run-script", methods=["POST"])
def run_script():
    """Clears the upload folder and runs test.py"""
    clear_upload_folder()
    
    # Run the script in a separate thread
    subprocess.Popen(["python", "test_new.py"])

    return jsonify({"message": "Processing started!"})

@app.route("/invoke", methods=["POST"])
def invoke():
    """Fetches the already uploaded files and calls graph.invoke()"""
    if not os.path.exists(UPLOAD_FOLDER) or not os.listdir(UPLOAD_FOLDER):
        return jsonify({"error": "No files found in upload folder"}), 400
    
    # Fetch uploaded files
    uploaded_files = [os.path.join(UPLOAD_FOLDER, file) for file in os.listdir(UPLOAD_FOLDER)]
    ids = [os.path.splitext(os.path.basename(file))[0] for file in uploaded_files]

    df = pd.read_csv("public/spotify_songs.csv")
    filtered_df = df[df["track_id"].isin(ids)]
    result = {
    "sections": [{"audio_file": f"{UPLOAD_FOLDER}/{track_id}.mp3"} for track_id in filtered_df["track_id"]],
    "final_playlist_sub_genre": filtered_df["playlist_subgenre"].tolist(),
    "final_danceability": filtered_df["danceability"].tolist(),
    "final_energy": filtered_df["energy"].tolist(),
    "final_key": filtered_df["key"].tolist(),
    "final_loudness": filtered_df["loudness"].tolist(),
    "final_mode": filtered_df["mode"].tolist(),
    "final_speechiness": filtered_df["speechiness"].tolist(),
    "final_acousticness": filtered_df["acousticness"].tolist(),
    "final_instrumentalness": filtered_df["instrumentalness"].tolist(),
    "final_liveness": filtered_df["liveness"].tolist(),
    "final_valence": filtered_df["valence"].tolist(),
    "final_tempo": filtered_df["tempo"].tolist(),
    }
    
    # return result
    graph.invoke(result)
    return jsonify({"message": "Processing started with graph.invoke!"})





@app.route('/playlist', methods=['POST'])
def get_playlist_url():
    data = request.get_json()
    playlist_url = data.get("url")

    if not playlist_url:
        return jsonify({"message": "No URL provided"}), 400

    playlist_id = playlist_url[34:56]  # Extracting playlist ID

    # Pass playlist_id as an argument to playlist.py
    subprocess.Popen(["python", "playlist.py", playlist_id])

    return jsonify({"message": "Playlist process started!"}), 200










@app.route('/musicgen_out.wav')
def serve_audio():
    return send_file("C:/Users/bhave/Documents/Epoch 2.0/nextjs-audio-upload1/server_musicgen_out.wav", mimetype="audio/wav")

if __name__ == "__main__":
    app.run(debug=True)

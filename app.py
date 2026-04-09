from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import yt_dlp

app = Flask(__name__)
CORS(app)

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL"}), 400

    video_id = str(uuid.uuid4())
    file_path = os.path.join(OUTPUT_FOLDER, f"{video_id}.mp4")

    ydl_opts = {
        "outtmpl": file_path,
        "format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # We are NOT cutting on server anymore (to keep it stable)
    # Instead we return the video directly

    return jsonify({
        "file": f"/download/{video_id}.mp4"
    })

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

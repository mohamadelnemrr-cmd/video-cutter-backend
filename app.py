from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")

    ydl_opts = {
        'outtmpl': video_path,
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    clip = VideoFileClip(video_path)
    duration = int(clip.duration)

    links = []

    for i in range(0, duration, 5):
        subclip = clip.subclip(i, min(i+5, duration))
        out_name = f"{uuid.uuid4()}.mp4"
        out_path = os.path.join(OUTPUT_FOLDER, out_name)
        subclip.write_videofile(out_path, codec="libx264", audio_codec="aac")

        links.append(f"/download/{out_name}")

    return jsonify({"files": links})

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

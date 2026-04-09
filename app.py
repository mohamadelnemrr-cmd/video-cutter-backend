from flask import Flask, request, jsonify
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["video"]
    filename = str(uuid.uuid4()) + ".mp4"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    clip = VideoFileClip(path)
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
    return app.send_static_file(os.path.join(OUTPUT_FOLDER, filename))

if __name__ == "__main__":
    app.run()
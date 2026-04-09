from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "backend running"})

@app.route("/cut", methods=["POST"])
def cut():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data["url"]

        # TEMP RESPONSE (we will add real cutting later)
        return jsonify({
            "status": "success",
            "message": "Video received",
            "video_url": url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()

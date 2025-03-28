from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import time

app = Flask(__name__)

AUDIO_FOLDER = "static/audio"
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    timestamp = int(time.time())

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        
        if text:
            filename_mp3 = f"speech_{timestamp}.mp3"
            mp3_path = os.path.join(AUDIO_FOLDER, filename_mp3)

            # Convert text to speech using gTTS
            tts = gTTS(text=text, lang="en")
            tts.save(mp3_path)

            audio_file = f"/static/audio/{filename_mp3}"

    return render_template("index.html", audio_file=audio_file, timestamp=timestamp)

@app.route("/audio/<filename>")
def get_audio(filename):
    audio_path = os.path.join(AUDIO_FOLDER, filename)
    return send_file(audio_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)

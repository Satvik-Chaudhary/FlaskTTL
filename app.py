from flask import Flask, render_template, request, send_file
import pyttsx3
import os
import time

app = Flask(__name__)

# Directory to store generated audio files
AUDIO_FOLDER = "static/audio"
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    timestamp = int(time.time())  # Cache busting for the audio file

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        
        if text:
            filename = f"speech_{timestamp}.mp3"
            audio_path = os.path.join(AUDIO_FOLDER, filename)
            
            # Convert text to speech
            engine = pyttsx3.init()
            engine.save_to_file(text, audio_path)
            engine.runAndWait()

            # Return the generated audio file
            audio_file = f"/static/audio/{filename}"

    return render_template("index.html", audio_file=audio_file, timestamp=timestamp)

# Route to serve the audio file
@app.route("/audio/<filename>")
def get_audio(filename):
    audio_path = os.path.join(AUDIO_FOLDER, filename)
    return send_file(audio_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)

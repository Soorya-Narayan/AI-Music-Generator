from flask import Flask, render_template, request, jsonify
import requests
import os
import serial
import threading

app = Flask(__name__)
COLAB_ENDPOINT = "https://3538-34-150-233-19.ngrok-free.app/receive"  # replace with your actual endpoint

# Serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Change 'COM3' as needed

# Stores selected inputs
selected_inputs = {
    "instrument": None,
    "mood": None,
    "genre": None
}

# Key mapping
KEY_LABELS = {
    '1': ('instrument', 'Guitar'),
    '2': ('instrument', 'Drums'),
    '3': ('instrument', 'Violin'),
    '4': ('instrument', 'Piano'),
    '5': ('mood', 'Happy'),
    '6': ('mood', 'Sad'),
    '7': ('mood', 'Angry'),
    '8': ('mood', 'Calm'),
    '9': ('genre', 'Pop'),
    'A': ('genre', 'Jazz'),
    'B': ('genre', 'Rock'),
    'C': ('genre', 'Classical'),
    'D': ('control', 'Pause'),
    'E': ('control', 'Play'),
    'F': ('control', 'Reset'),
    'G': ('control', 'Generate')
}

# Background thread: listen to Arduino
def read_serial():
    while True:
        if ser.in_waiting:
            key = ser.readline().decode().strip()
            if key in KEY_LABELS:
                category, label = KEY_LABELS[key]
                if category in selected_inputs:
                    selected_inputs[category] = label
                elif label == 'Reset':
                    for k in selected_inputs:
                        selected_inputs[k] = None
                elif label == 'Generate':
                    generate_music_from_inputs()

def generate_music_from_inputs():
    if None in selected_inputs.values():
        print("Incomplete inputs.")
        return

    data = {
        "genre": selected_inputs["genre"],
        "instrument": [selected_inputs["instrument"]],
        "mood": selected_inputs["mood"],
        "duration": 10
    }

    try:
        response = requests.post(COLAB_ENDPOINT, json=data)
        if response.status_code == 200:
            music_path = os.path.join("static", "generated_music.wav")
            with open(music_path, "wb") as f:
                f.write(response.content)
            print("✅ Music generated.")
        else:
            print("❌ Failed to generate music.")
    except Exception as e:
        print("🔥 Error:", e)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/selections")
def get_selections():
    return jsonify(selected_inputs)

@app.route("/submit", methods=["POST"])
def manual_submit():
    # This allows manual UI fallback submission (if needed)
    genre = request.form.get("genre")
    instrument = request.form.get("instrument")
    mood = request.form.get("mood")

    data = {
        "genre": genre,
        "instrument": [instrument],
        "mood": mood,
        "duration": 10
    }

    try:
        response = requests.post(COLAB_ENDPOINT, json=data)
        if response.status_code == 200:
            music_path = os.path.join("static", "generated_music.wav")
            with open(music_path, "wb") as f:
                f.write(response.content)

            return jsonify({
                "message": "Music generated",
                "file": "/static/generated_music.wav"
            })
        else:
            return jsonify({"error": "Failed to generate music"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    threading.Thread(target=read_serial, daemon=True).start()
    app.run(debug=True)

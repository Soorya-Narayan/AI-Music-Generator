# 🎵 AI Music Generator
 
> An interactive AI-powered music synthesizer that generates real-time music based on your selected **mood**, **genre**, and **instrument** — controlled via a physical keypad (Arduino) connected to a Raspberry Pi, with audio playback through a web interface.

<table align="center">
  <tr>
    <td align="center"><img src="assets/Screenshot 2025-03-12 110349.png" width="280" height="200" /></td>
    <td align="center"><img src="assets/circuit_image-transformed (1).png" width="280" height="200" /></td>
  </tr>
</table>

---

## 📖 Overview
 
The AI Music Generator is a hardware-software hybrid system that bridges physical input with AI-driven music composition. A user selects their desired instrument, mood, and genre using a 4×4 matrix keypad wired to an **Arduino**, which relays the input over serial USB to a **Raspberry Pi**. The Pi runs a Flask web server that forwards the selections to an AI model (hosted on Google Colab via ngrok), which composes and returns a `.wav` audio file — playable in real time through the browser UI served by the Pi.
 
---
 
## ✨ Features
 
- 🎹 **4 Instruments** — Guitar, Drums, Violin, Piano
- 🎭 **4 Moods** — Happy, Sad, Angry, Calm
- 🎶 **4 Genres** — Pop, Jazz, Rock, Classical
- ⚡ **Real-time generation** via AI model on Google Colab
- 🖥️ **Web UI** with live selection display and audio playback
- 🔌 **Hardware control** via Arduino 4×4 keypad → Raspberry Pi over serial
- 🔁 **Manual web fallback** — works without the Arduino too
---
 
## 🏗️ System Architecture
 
```
┌─────────────────┐     Serial (USB)     ┌──────────────────────────┐
│  Arduino Uno    │ ──────────────────►  │  Raspberry Pi            │
│  4×4 Keypad     │                      │  Flask Server (app.py)   │
└─────────────────┘                      │  Web UI  (index.html)    │
                                         └──────────┬───────────────┘
                                                    │  HTTP (ngrok)
                                                    ▼
                                         ┌──────────────────────────┐
                                         │  Google Colab            │
                                         │  AI Music Model          │
                                         │  → returns .wav          │
                                         └──────────────────────────┘
```
 
**Data flow:**
1. User presses keys on the Arduino-connected keypad to choose instrument, mood, and genre.
2. Arduino sends the key character over serial USB to the Raspberry Pi.
3. The Pi's Flask server reads the serial input and updates the current selections.
4. On `Generate` (key `G`), Flask POSTs the selections to the Colab AI endpoint.
5. The AI model returns a `.wav` file, saved to `/static/generated_music.wav`.
6. The browser UI (served by Flask on the Pi) polls `/selections` every second and plays the audio.
---
 
## 🎛️ Keypad Layout
 
The 4×4 keypad maps to the following inputs:
 
| Key | Category   | Selection    |
|-----|------------|--------------|
| `1` | Instrument | Guitar       |
| `2` | Instrument | Drums        |
| `3` | Instrument | Violin       |
| `4` | Instrument | Piano        |
| `5` | Mood       | Happy        |
| `6` | Mood       | Sad          |
| `7` | Mood       | Angry        |
| `8` | Mood       | Calm         |
| `9` | Genre      | Pop          |
| `A` | Genre      | Jazz         |
| `B` | Genre      | Rock         |
| `C` | Genre      | Classical    |
| `D` | Control    | Pause        |
| `E` | Control    | Play         |
| `F` | Control    | Reset        |
| `G` | Control    | **Generate** 🎵 |
 
---
 
## 📁 Project Structure
 
```
AI-Music-Generator/
├── app.py                  # Flask backend + serial listener (runs on Raspberry Pi)
├── arduino_keypad.ino      # Arduino sketch for 4×4 keypad
├── index.html              # Web frontend (live selections + audio player)
├── assets/
│   ├── Screenshot 2025-03-12 110349.png
│   └── circuit_image-transformed (1).png
└── README.md
```
 
---
 
## 🛠️ Setup & Installation
 
### Hardware Required
 
- Raspberry Pi (any model with USB; Pi 3B+ or Pi 4 recommended)
- Arduino Uno
- 4×4 Matrix Keypad
- USB-A to USB-B cable (Arduino ↔ Pi)
- Speakers or headphones connected to the Pi
### Software Prerequisites
 
- Python 3.8+ (on the Raspberry Pi)
- Arduino IDE (on any machine to flash the sketch)
- Google Colab (for running the AI model)
- ngrok (to expose the Colab endpoint publicly)
---
 
### 1. Clone the Repository (on the Raspberry Pi)
 
```bash
git clone https://github.com/Soorya-Narayan/AI-Music-Generator.git
cd AI-Music-Generator
```
 
### 2. Install Python Dependencies
 
```bash
pip install flask pyserial requests
```
 
### 3. Flash the Arduino
 
1. Open `arduino_keypad.ino` in the Arduino IDE.
2. Install the **Keypad** library via the Library Manager (`Sketch → Include Library → Manage Libraries → search "Keypad"`).
3. Wire the 4×4 matrix keypad to the Arduino using the following pins:
   - **Row pins:** 22, 24, 26, 28
   - **Column pins:** 30, 32, 34, 36
4. Connect the Arduino to the Raspberry Pi via USB and upload the sketch.
### 4. Start the AI Model on Google Colab
 
Run your AI music generation model on Google Colab and expose it with ngrok:
 
```python
from pyngrok import ngrok
public_url = ngrok.connect(5000)
print("Endpoint:", public_url)
```
 
Copy the generated ngrok URL.
 
### 5. Configure the Flask App
 
In `app.py`, update the Colab endpoint and the serial port for your Arduino:
 
```python
COLAB_ENDPOINT = "https://<your-ngrok-url>/receive"
 
# On Raspberry Pi, Arduino is typically /dev/ttyUSB0 or /dev/ttyACM0
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
```
 
> **Tip:** Run `ls /dev/tty*` before and after plugging in the Arduino to identify the correct port.
 
### 6. Run the Flask Server on the Raspberry Pi
 
```bash
python app.py
```
 
Open a browser on any device on the same network and navigate to:
 
```
http://<raspberry-pi-ip>:5000
```
 
---
 
## 🚀 Usage
 
**Using the Arduino keypad:**
1. Press a key from row 1 (`1`–`4`) to select an **instrument**.
2. Press a key from row 2 (`5`–`8`) to select a **mood**.
3. Press a key from row 3 (`9`, `A`, `B`, `C`) to select a **genre**.
4. Press `G` to **generate** the music.
5. The generated audio will appear in the browser and play automatically.
**Using the Web UI only (no Arduino required):**
Select your instrument, mood, and genre directly from the browser and click **Generate**.
 
---
 
## 🔌 API Endpoints
 
| Method | Endpoint      | Description                                      |
|--------|---------------|--------------------------------------------------|
| `GET`  | `/`           | Serves the web frontend                          |
| `GET`  | `/selections` | Returns current keypad selections as JSON        |
| `POST` | `/submit`     | Manual submission from web UI to generate music  |
 
---
 
## 🧰 Tech Stack
 
| Layer        | Technology                                    |
|--------------|-----------------------------------------------|
| Hardware     | Arduino Uno, 4×4 Matrix Keypad                |
| Middleware   | Raspberry Pi (Flask server + serial bridge)   |
| Firmware     | C++ (Arduino / Keypad library)                |
| Backend      | Python, Flask, PySerial                       |
| AI Model     | Google Colab + ngrok                          |
| Frontend     | HTML, CSS, JavaScript                         |
| Audio Output | WAV file via HTML `<audio>` element           |
 
---
 
## 🤝 Contributing
 
Contributions are welcome! Feel free to open an issue or submit a pull request for bug fixes, new features, or improvements.
 
1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request
---
 
## 📄 License
 
This project is open source. See the repository for license details.
 
---

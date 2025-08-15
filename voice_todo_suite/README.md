
# Voice To‑Do Suite (Python + Frontend)

This bundle gives you **both**:
1. **Desktop app (PyQt5)** — voice to‑do list with **online (Google)** and **offline (Vosk)** speech.
2. **Web frontend** — runs in the browser using the Web Speech API (no Python needed).
3. **Optional Flask server** — serves the web frontend locally via Python.

## Structure
```
voice_todo_suite/
├─ desktop_pyqt/       # PyQt5 desktop apps
│  ├─ app.py           # online (Google Speech Recognition)
│  ├─ app_vosk.py      # offline (Vosk + sounddevice)
│  ├─ requirements.txt
│  └─ README.md
├─ web/                # HTML/CSS/JS web app
│  ├─ index.html
│  ├─ style.css
│  └─ script.js
└─ server_flask/       # Simple Flask server for the web app
   ├─ app.py
   └─ requirements.txt
```

## Quick Start

### Desktop (recommended)
```bash
cd desktop_pyqt
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt

# Online mode
python app.py

# Offline mode (download model first)
# Download a Vosk model (e.g., vosk-model-small-en-us-0.15) and extract into this folder
python app_vosk.py
```

### Web (no installs)
Open `web/index.html` in Chrome and click **Start Voice**.

### Flask server (optional)
```bash
cd server_flask
python -m venv .venv
# activate venv ...
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000
```

## Notes
- On Windows, if `PyAudio` fails, install via `pipwin` or use the Vosk offline app which uses `sounddevice` instead.
- For offline: place the extracted Vosk model folder alongside `app_vosk.py`.

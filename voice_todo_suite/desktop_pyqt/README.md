
# Desktop App (PyQt5)

Two launch options:
- `app.py` — Online recognition via Google (needs internet + PyAudio)
- `app_vosk.py` — Offline recognition via Vosk (needs `vosk` + `sounddevice` and a downloaded Vosk model)

### Install (Windows/macOS/Linux)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Vosk Model
Download a model (e.g. `vosk-model-small-en-us-0.15`) from https://alphacephei.com/vosk/models and extract into this folder so it sits as:
```
desktop_pyqt/
  app_vosk.py
  vosk-model-small-en-us-0.15/
```

### Run
```bash
python app.py       # online
python app_vosk.py  # offline
```

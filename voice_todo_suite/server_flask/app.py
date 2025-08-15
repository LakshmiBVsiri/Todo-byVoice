#!/usr/bin/env python3
# Serve the web frontend with Flask (no backend recognition, handled in browser)
from flask import Flask, send_from_directory
from pathlib import Path

# Paths
WEB_FOLDER = Path(__file__).parent / "web"

app = Flask(__name__, static_folder=str(WEB_FOLDER), static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico")

# Serve other static assets (CSS, JS, images, etc.)
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    # Run: python app.py then open http://127.0.0.1:5000
    app.run(debug=True)

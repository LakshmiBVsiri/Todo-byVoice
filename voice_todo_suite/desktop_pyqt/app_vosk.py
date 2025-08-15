#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice-Controlled To-Do List (PyQt5 + Vosk Offline)
"""
import sys
import json
from pathlib import Path
import queue

import vosk
import sounddevice as sd
import pyttsx3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox,
    QHBoxLayout, QFileDialog, QLabel
)

SAVE_FILE = Path("tasks.json")
MODEL_PATH = Path("vosk-model-small-en-us-0.15")  # Download & extract into project folder

tts = pyttsx3.init()

def speak(text: str) -> None:
    try:
        tts.say(text)
        tts.runAndWait()
    except Exception:
        pass

class VoiceTodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice To-Do (Offline - Vosk)")
        self.resize(520, 420)

        self._build_ui()
        self._apply_dark_theme()
        self._load_tasks()

        if not MODEL_PATH.exists():
            QMessageBox.critical(self, "Model Missing",
                                 f"Vosk model not found at {MODEL_PATH}.\n"
                                 "Download from https://alphacephei.com/vosk/models and extract here.")
            sys.exit(1)
        self.model = vosk.Model(str(MODEL_PATH))

    def _build_ui(self):
        layout = QVBoxLayout(self)

        header = QLabel("🎤 Offline speech via Vosk — click “Add Task (Voice)” and speak")
        header.setWordWrap(True)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.task_list)

        row = QHBoxLayout()
        self.add_btn = QPushButton("Add Task (Voice)")
        self.add_btn.clicked.connect(self.listen_task)
        row.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        row.addWidget(self.delete_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        row.addWidget(self.clear_btn)

        layout.addLayout(row)

        files = QHBoxLayout()
        self.save_btn = QPushButton("Save As…")
        self.save_btn.clicked.connect(self.save_as)
        files.addWidget(self.save_btn)

        self.open_btn = QPushButton("Open…")
        self.open_btn.clicked.connect(self.open_file)
        files.addWidget(self.open_btn)

        layout.addLayout(files)

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background: #0b1020; color: #e6e9f2; font-size: 14px; }
            QListWidget { background: #12192f; border: 1px solid #1e2641; }
            QPushButton {
                background: #1a2342; border: 1px solid #2b3767; padding: 8px 12px;
                border-radius: 10px;
            }
            QPushButton:hover { background: #222d56; }
            QPushButton:pressed { background: #2a376d; }
            QLabel { color: #cfd5ea; }
        """)

    def _load_tasks(self, file_path: Path = SAVE_FILE):
        try:
            if Path(file_path).exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.task_list.clear()
                for item in data.get("tasks", []):
                    self.task_list.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Could not load tasks:\n{e}")

    def _save_tasks(self, file_path: Path = SAVE_FILE):
        try:
            tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Could not save tasks:\n{e}")

    def listen_task(self):
        speak("Listening for your task.")
        q = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        try:
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=callback):
                rec = vosk.KaldiRecognizer(self.model, 16000)
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").strip()
                        if text:
                            self.task_list.addItem(text)
                            speak(f"Task added: {text}")
                        break
        except Exception as e:
            QMessageBox.critical(self, "Audio Error", str(e))

    def delete_selected(self):
        items = self.task_list.selectedItems()
        if not items:
            QMessageBox.information(self, "No Selection", "Select one or more tasks to delete.")
            return
        for item in items:
            self.task_list.takeItem(self.task_list.row(item))
        speak("Task deleted.")

    def clear_all(self):
        if self.task_list.count() == 0:
            return
        confirm = QMessageBox.question(self, "Clear All", "Delete all tasks?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.task_list.clear()
            speak("All tasks cleared.")

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Tasks", str(SAVE_FILE), "JSON Files (*.json)")
        if path:
            self._save_tasks(Path(path))

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Tasks", "", "JSON Files (*.json)")
        if path:
            self._load_tasks(Path(path))

    def closeEvent(self, event):
        self._save_tasks(SAVE_FILE)
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = VoiceTodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

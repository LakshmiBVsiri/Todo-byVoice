#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice-Controlled To-Do List (PyQt5)
- Add tasks using your voice (Google Speech Recognition)
- Delete selected tasks
- Autosaves tasks to tasks.json on exit; loads on startup
- Simple dark theme
"""
import sys
import json
from pathlib import Path

import speech_recognition as sr
import pyttsx3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox,
    QHBoxLayout, QFileDialog, QLabel
)

SAVE_FILE = Path("tasks.json")

# Initialize recognizer and TTS engine (global so it initializes once)
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text: str) -> None:
    try:
        tts.say(text)
        tts.runAndWait()
    except Exception:
        # If TTS backend isn't available, fail silently
        pass

class VoiceTodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice-Controlled To-Do List")
        self.resize(520, 420)

        self._build_ui()
        self._apply_dark_theme()
        self._load_tasks()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        header = QLabel("🎤 Say your task after you click “Add Task (Voice)”")
        header.setWordWrap(True)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.task_list)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("Add Task (Voice)")
        self.add_btn.clicked.connect(self.listen_task)
        btn_row.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        btn_row.addWidget(self.delete_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        btn_row.addWidget(self.clear_btn)

        layout.addLayout(btn_row)

        file_row = QHBoxLayout()
        self.save_btn = QPushButton("Save As…")
        self.save_btn.clicked.connect(self.save_as)
        file_row.addWidget(self.save_btn)

        self.open_btn = QPushButton("Open…")
        self.open_btn.clicked.connect(self.open_file)
        file_row.addWidget(self.open_btn)

        layout.addLayout(file_row)

    def _apply_dark_theme(self):
        # A light-weight dark stylesheet
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

    # -------- Persistence --------
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

    # -------- Actions --------
    def listen_task(self):
        try:
            with sr.Microphone() as source:
                speak("Listening for your task.")
                # Reduce noise impact
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            speak("No speech detected.")
            QMessageBox.information(self, "Timeout", "No speech detected. Try again.")
            return
        except Exception as e:
            QMessageBox.warning(self, "Microphone Error", f"Microphone not available or busy.\n{e}")
            return

        try:
            # Uses Google Web Speech API (internet required)
            task = recognizer.recognize_google(audio)
            task = task.strip()
            if task:
                self.task_list.addItem(task)
                speak(f"Task added: {task}")
            else:
                speak("I heard nothing.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
            QMessageBox.information(self, "Didn't catch that", "Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            speak("Speech recognition service unavailable.")
            QMessageBox.critical(self, "Network Error", f"Speech service unavailable:\n{e}")

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

    # -------- Lifecycle --------
    def closeEvent(self, event):
        # Autosave on close
        self._save_tasks(SAVE_FILE)
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = VoiceTodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

"""
Minimal Flask server to expose the keyword-based emotion detector.
Includes an optional static analysis helper for assignment demonstrations.
"""
from __future__ import annotations

import os
import subprocess
from typing import Any, Dict

from flask import Flask, jsonify, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> Any:
    return jsonify({"message": "Emotion detection service is running."})


@app.route("/emotionDetector", methods=["POST"])
def detect_emotion() -> Any:
    payload: Dict[str, Any] = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    result = emotion_detector(text)
    if result.get("status") == 400:
        return jsonify(result), 400
    return jsonify(result)


def run_static_code_analysis() -> str:
    """
    Execute pylint over the package and server module.
    Returns collected output so it can be printed or logged.
    """
    command = ["pylint", "EmotionDetection", "server.py"]
    try:
        completed = subprocess.run(
            command, check=False, capture_output=True, text=True
        )
    except FileNotFoundError:
        return "pylint not installed; static analysis skipped."

    output = completed.stdout or ""
    if completed.stderr:
        output += completed.stderr
    return output


if __name__ == "__main__":
    if os.getenv("RUN_STATIC_ANALYSIS") == "1":
        print(run_static_code_analysis())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)

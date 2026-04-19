"""
Lightweight emotion detector used for assignment demonstrations.
The implementation is keyword-based to keep the package self-contained.
"""
from __future__ import annotations

import re
from typing import Dict, Optional

# Simple keyword map that approximates how different emotions are expressed.
EMOTION_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "anger": ("angry", "furious", "rage", "irritated", "mad"),
    "disgust": ("disgust", "gross", "nasty", "revolting", "sickening"),
    "fear": ("afraid", "scared", "fear", "terrified", "nervous"),
    "joy": ("happy", "joy", "joyful", "delight", "glad", "excited", "cheerful"),
    "sadness": ("sad", "unhappy", "depressed", "down", "gloomy", "sadness"),
}


def _score_emotions(text: str) -> Dict[str, float]:
    """Return normalized keyword scores for each emotion."""
    counts = {emotion: 0 for emotion in EMOTION_KEYWORDS}
    lowered = text.lower()

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            counts[emotion] += len(re.findall(rf"\b{re.escape(keyword)}\b", lowered))

    total = sum(counts.values())
    if total == 0:
        return {emotion: 0.0 for emotion in counts}

    return {emotion: round(count / total, 3) for emotion, count in counts.items()}


def emotion_detector(text: Optional[str]) -> Dict[str, Optional[float] | Optional[str] | int]:
    """
    Basic emotion detector used to mimic Watson NLP output shape.

    Returns a dictionary with scores for anger, disgust, fear, joy, and sadness,
    plus the dominant emotion and an HTTP-like status code. Empty or missing
    input yields a 400-style response with null scores.
    """
    if text is None or text.strip() == "":
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status": 400,
            "error": "Invalid request: text is empty.",
        }

    scores = _score_emotions(text)
    dominant_emotion = max(scores, key=scores.get) if any(scores.values()) else None

    return {
        **scores,
        "dominant_emotion": dominant_emotion,
        "status": 200,
    }

from EmotionDetection import emotion_detector


def test_emotion_detector_returns_scores_and_dominant():
    text = "I am happy and joyful but only a little sad."
    result = emotion_detector(text)

    assert result["status"] == 200
    assert result["dominant_emotion"] == "joy"
    assert result["joy"] > result["sadness"]
    assert set(result).issuperset({"anger", "disgust", "fear", "joy", "sadness"})


def test_emotion_detector_handles_empty_input():
    result = emotion_detector("   ")

    assert result["status"] == 400
    assert result["dominant_emotion"] is None
    assert all(
        result[emotion] is None for emotion in ["anger", "disgust", "fear", "joy", "sadness"]
    )

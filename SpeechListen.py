import speech_recognition as sr


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        r.non_speaking_duration = 0.2
        r.pause_threshold = 0.2
        r.adjust_for_ambient_noise(source=mic, duration=0.2)

        audio = r.listen(source=mic)
    try:
        com = r.recognize_google(audio, language='ru-RU').lower()
    except sr.UnknownValueError:
        return None
    return com
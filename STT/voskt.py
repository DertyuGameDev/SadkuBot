import sys
import os
import wave
import json
from vosk import Model, KaldiRecognizer


model = Model("../VOST")
rec = KaldiRecognizer(model, 16000)

# Открытие аудиопотока
wf = wave.open("../audio_0.mp3", "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

# Обработка аудиопотока
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        print(result)
    else:
        print(rec.PartialResult())

# Финальный результат
print(rec.FinalResult())
import os
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import WhiteNoise

def generate_audio_with_noise(text, filename, noise_level=0.1):
    # Генерация аудиофайла с текстом
    tts = gTTS(text=text, lang='ru')
    tts.save(filename)

    # Загрузка сгенерированного аудиофайла
    audio = AudioSegment.from_file(filename)

    # Генерация белого шума
    noise = WhiteNoise().to_audio_segment(duration=len(audio))

    # Применение шума к аудиофайлу
    noisy_audio = audio.overlay(noise - (noise_level * 100))  # Уменьшение уровня шума

    # Сохранение аудиофайла с шумом
    noisy_filename = f"noisy_{filename}"
    noisy_audio.export(noisy_filename, format="wav")

    print(f"Сгенерирован аудиофайл: {noisy_filename}")

# Пример использования
texts = [
    "Привет, как дела? проверка текста. давай проверим. отведай этих сладких французких булок, да выпей чаю!",
]

# Генерация аудиофайлов с шумом
for i, text in enumerate(texts):
    generate_audio_with_noise(text, f"audio_{i}.mp3")
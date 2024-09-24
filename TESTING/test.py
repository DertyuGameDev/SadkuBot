import gtts
import pyaudio
import wave
import pygame
from ShazamAPI import Shazam


class MyShazam:
    def __init__(self, file_path, record_seconds):
        self.file_path = file_path
        self.record_seconds = record_seconds
        pygame.mixer.init()

    def record_audio(self):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 16000  # Record at 16000 samples per second

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True,
                        input_device_index=1)

        frames = []  # Initialize array to store frames

        # Store data in chunks for record_seconds seconds
        for _ in range(0, int(fs / chunk * self.record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        with wave.open(self.file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))

    def shazam_recognize(self):
        with open(self.file_path, 'rb') as fp:
            mp3_file_content_to_recognize = fp.read()

        shazam = Shazam(mp3_file_content_to_recognize)
        recognize_generator = shazam.recognizeSong()

        for offset, resp in recognize_generator:
            if resp and 'track' in resp:
                return resp['track']['title'], resp['track']['subtitle']
        return None

    def playSound(self, song_title, text):
        tts = gtts.gTTS(text, lang='ru')
        tts.save('sound.mp3')
        pygame.mixer.music.load(f'sound.mp3')
        pygame.mixer.music.play()

    def recognize_all_song(self):
        while True:
            audio_file = 'recorded_audio.wav'
            self.record_audio()
            song_title = self.shazam_recognize()
            if song_title:
                self.playSound(song_title, f'Вы искали {song_title[0]} от {song_title[1]}')
                break
            else:
                continue
        while pygame.mixer.music.get_busy():
            continue


shaz = MyShazam('recorded_audio.wav', 5)
shaz.recognize_all_song()
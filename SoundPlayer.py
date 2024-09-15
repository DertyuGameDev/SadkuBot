import os

import pygame

pygame.mixer.init()

def play_sound(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    else:
        print(f"File {file_path} does not exist.")
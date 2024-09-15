import os
import threading
import webbrowser
import wmi
from g4f.client import Client
from gtts import gTTS

from WriteReadJson import writeall, read
from SoundPlayer import play_sound


class Command:
    def __init__(self, command, *word, id):
        self.word = [*word]
        self.command = command
        self.id = id;

    def getCommand(self):
        return self.word

    def setWords(self, words):
        self.word = words

    def getID(self):
        return self.id

    def __call__(self, word):
        self.command(word)


class CommandManager:
    def __init__(self):
        self.commands = []

    def addCommand(self, com: Command):
        if com not in self.commands:
            self.commands.append(com)
        return None

    def removeCommand(self, com: Command):
        if com in self.commands:
            self.commands.remove(com)
        return None

    def search(self, text):
        for i in self.commands:
            for j in i.getCommand():
                if j in text:
                    i(j)
                    return
        return None

    def lastID(self):
        if self.commands:
            return self.commands[-1].getID()
        return -1

    def __str__(self):
        for i in self.commands:
            print(i.getCommand(), i.id, '\n')
        return ''

def fillCommandManager(ComMan, commands):
    o = 0
    for i in commands.keys():
        c1 = Command(i, *commands[i], id=o)
        o += 1
        ComMan.addCommand(c1)


def browser(link1):
    play_sound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
    webbrowser.open(new=1, url=link1)


def openApp(path):
    play_sound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
    os.startfile(path)


def thanks():
    play_sound('Sounds/Recording.mp3')


def closeApp(text):
    text = text.lower()  # Convert the input once
    process = wmi.WMI()
    for i in process.Win32_Process(Name=f"{text}.exe"):  # Filter process by name
        os.system(f"taskkill /im {i.Name} /f")
        play_sound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
        return


client = Client()


def gpt(text):
    text = ' '.join(text.split()[1:])
    play_sound('Sounds/ichu_[cut_1sec].mp3')
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"{text}?"}]
    )
    tts = gTTS(response.choices[0].message.content, lang='ru')
    tts.save(f'Sounds/{text}.mp3')
    play_sound('Sounds/otv_[cut_1sec].mp3')
    file = open('gptAnswers/AllOtv.txt', 'w+')
    file.writelines(text + '\n')
    file.writelines(response.choices[0].message.content)
    t = threading.Thread(target=play_sound, args=(f'Sounds/{text}.mp3',))
    t.start()


def searchInGoogle(text):
    play_sound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
    webbrowser.open(new=1, url=f'https://yandex.ru/search/?text={' '.join(text.split()[1:])}')


def searchInYoutube(text):
    play_sound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
    print(' '.join(text.split()[3:]))
    webbrowser.open(new=1, url=f'https://www.youtube.com/results?search_query={' '.join(text.split()[3:])}')

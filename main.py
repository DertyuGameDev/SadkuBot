#!/usr/bin/python
# -*- coding: utf8 -*-
import asyncio
import os
import sys
import threading
import playsound3
import pygame
from gtts import gTTS
import webbrowser
from g4f.client import Client
import eel
import wmi
from SoundPlayer import play_sound
from Command import CommandManager, Command, thanks, browser, openApp, closeApp, fillCommandManager, searchInGoogle, \
    searchInYoutube, gpt
import WriteReadJson
import SpeechListen

WriteReadJson.search()
text = ''
# commands = {
#     lambda x: browser('https://www.youtube.com/'): ['запусти youtube', 'включи youtube', 'открой youtube'],
#     lambda x: browser('https://vk.com/x36murmansk'): ['расписание'],
#     lambda x: openApp("C:\\\\Program Files\\Google\\Chrome\\Application\\chrome.exe"): ['запусти chrome',
#                                                                                         'включи chrome',
#                                                                                         'открой chrome'],
#     lambda x: openApp("C:\\\\Users\\Sviat\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"): ['запусти telegram',
#                                                                                                 'включи telegram',
#                                                                                                 'открой telegram'],
#     lambda x: openApp("C:\\\\Users\\Sviat\\AppData\\Local\\Programs\\Obsidian\\Obsidian.exe"): ['запусти obsidian',
#                                                                                                 'включи obsidian',
#                                                                                                 'открой obsidian'],
#     lambda x: gpt(text): ['gpt', 'гпт'],
#     lambda x: closeApp(' '.join(x.split()[1:])): ['закрой chrome'],
#     lambda x: closeApp(' '.join(x.split()[1:])): ['закрой telegram'],
#     lambda x: searchInYoutube(text): ['ищи в ютуби', 'ищи в ютюбе'],
#     lambda x: searchInGoogle(text): ['загугли', 'ищи'],
#     lambda x: thanks(): ['спасибо'],
# }

client = Client()
c = CommandManager()
# fillCommandManager(c, commands)

print('ok')


@eel.expose
def setCommandWords(words, id):
    print(words)
    for i in c.commands:
        i: Command
        if i.getID() == int(id):
            i.setWords(words.split(', '))

@eel.expose
def lastID():
    return c.lastID()


@eel.expose
def removeByID(id):
    for i in c.commands:
        if i.id == id:
            c.commands.remove(i)
            return None


@eel.expose
def add_task(num, url):
    if num == 0:
        c.addCommand(Command(lambda x: browser(url), id=c.lastID() + 1))
        return True


@eel.expose
def process_comands():
    global text
    while True:
        text = SpeechListen.listen()
        if text:
            try:
                c.search(text)
            except Exception as e:
                print(e)
                continue

            # if talkNow:
            #     if 'стоять' in text or 'стоп' in text or 'хватит' in text or 'стой' in text:
            #         talkNow = False
            #         pygame.mixer.music.stop()
            #         t = None
            # if gpt:
            #     playsound3.playsound('Sounds/ichu_[cut_1sec].mp3')
            #     response = client.chat.completions.create(
            #         model="gpt-4o",
            #         messages=[{"role": "user", "content": f"{text}?"}]
            #     )
            #     tts = gTTS(response.choices[0].message.content, lang='ru')
            #     tts.save(f'Sounds/{text}.mp3')
            #     playsound3.playsound('Sounds/otv_[cut_1sec].mp3')
            #     file = open('gptAnswers/AllOtv.txt', 'w+')
            #     file.writelines(text + '\n')
            #     file.writelines(response.choices[0].message.content)
            #     gpt = False
            #     t = threading.Thread(target=play_sound, args=(text,))
            #     t.start()
            # else:
            #     if 'запусти youtube' in text or 'включи youtube' in text or 'открой youtube' in text:
            #         playsound3.playsound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
            #         webbrowser.open(new=1, url='https://www.youtube.com/')
            #     if 'запусти игру' in text:
            #         playsound3.playsound('Sounds/play_[cut_1sec].mp3')
            #         game = True
            #     if ('искать' in text or 'загугли' in text) and len(text) > 6:
            #         playsound3.playsound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
            #         webbrowser.open(new=1, url=f'https://yandex.ru/search/?text={' '.join(text.split()[1:])}')
            #     if 'нейронка' in text or 'gpt' in text:
            #         playsound3.playsound('Sounds/search_[cut_1sec].mp3')
            #         gpt = True
            #     if 'закрой' in text or 'выключи' in text:
            #         for i in process.Win32_Process():
            #             if str(i.Name).replace('.exe', '').lower() in text.split(' ', maxsplit=1)[-1]:
            #                 os.system(f"taskkill /im {i.Name} /f")
            #         os.system(f"taskkill /im {text.split(' ', maxsplit=1)[1]}.exe /f")
            #     if 'включи' in text or 'запусти' in text or 'открой' in text:
            #         if len(text) > 7 and text.split(' ', maxsplit=1)[1] in WriteReadJson.read().keys():
            #             playsound3.playsound('Sounds/audio_2024-07-27_22-22-20_[cut_1sec].mp3')
            #             os.startfile(WriteReadJson.read()[text.split(' ', maxsplit=1)[1]])
            #     if 'спасибо' in text:
            #         # playsound3.playsound('Sounds/idi_[cut_1sec].mp3')
            #         playsound3.playsound('Sounds/Recording.mp3')
            #     if 'выключи компьютер' in text:
            #         os.system("shutdown /s /t 1")
            #     for c in commandsAll:
            #         c.startProg(text)
            print(c)
            print(text)


@eel.expose
def start_process_commands():
    threading.Thread(target=process_comands).start()


@eel.expose
def quit():
    sys.exit()


if __name__ == "__main__":
    eel.init('web')
    eel.start("main.html", size=(700, 700))

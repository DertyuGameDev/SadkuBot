import json
import os
import string
from ctypes import windll


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives


def writeall():
    d = dict()
    for k in get_drives():
        for dirpath, dirnames, filenames in os.walk(rf'{k}:\\'):
            for i in filenames:
                a = str(os.path.join(dirpath, i)).split("\\")[-1]
                if a in d.keys():
                    continue
                d[a] = str(os.path.join(dirpath, i))
    d = json.dumps(d)
    d = json.loads(str(d))
    with open('Jsons/result.json', '+w', encoding='utf-8') as fp:
        json.dump(d, fp, indent=3)


def read():
    with open('Jsons/result.json', 'r', encoding='utf-8') as fp:
        return json.load(fp)


def search():
    print('Подождите, пока мы загрузим все необходимое!')
    writeall()
    print('Все готово!')


def search_file(j):
    print(j)
    print(j)
    h = read()
    for i in h.keys():
        if i == j:
            return h[i]

import json
import os


def writeall(start_dir):
    d = dict()
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for i in filenames:
            if '.exe' in i:
                a = str(os.path.join(dirpath, i)).split("\\")[-1].split('.')[0].lower()
                d[a] = str(os.path.join(dirpath, i))
    d = json.dumps(d)
    d = json.loads(str(d))
    with open('Jsons/result.json', '+w', encoding='utf-8') as fp:
        json.dump(d, fp, indent=3)


def read():
    with open('Jsons/result.json', 'r', encoding='utf-8') as fp:
        return json.load(fp)


def search():
    if not os.path.exists('Jsons/result.json'):
        print('Подождите, пока мы загрузим все необходимое!')
        writeall(r'C:\\')
        print('Все готово!')
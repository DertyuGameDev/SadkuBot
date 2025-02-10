import os    
import sys
import winshell


def get_script_path():
    script_path = os.path.abspath(__file__)
    return script_path


def create_bat_file(script_path, bat_file_path):
    with open(bat_file_path, 'w') as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(f'python "{script_path}"\n')
        bat_file.write('pause\n')  # Оставляет окно открытым после выполнения


def add_to_startup(script_path):
    # Получаем путь к папке автозапуска
    startup_folder = winshell.startup()
    
    # Создаем имя ярлыка
    script_name = os.path.basename(script_path).replace('.py', '')  # Убираем .py
    shortcut_path = os.path.join(startup_folder, f'{script_name}.lnk')
    
    # Создаем ярлык
    shell = winshell.shell()
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = sys.executable  # Путь к интерпретатору Python
    shortcut.Arguments = f'"{script_path}"'  # Аргументы для запуска скрипта
    shortcut.WorkingDirectory = os.path.dirname(script_path)  # Рабочая директория
    shortcut.IconLocation = sys.executable  # Иконка
    shortcut.save()


def setup_autostart():
    # Путь к BAT-файлу
    bat_file_path = os.path.join(os.path.dirname(get_script_path()), 'run_script.bat')
    
    # Создаем BAT-файл
    create_bat_file(get_script_path(), bat_file_path)
    
    # Добавляем скрипт в автозапуск
    add_to_startup(get_script_path())
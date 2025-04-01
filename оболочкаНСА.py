import os
import sys
import getpass
import termcolor
from termcolor import *
import readline
import alsaaudio
import subprocess
import rlcompleter
import configparser 

CONFIG_FILE = os.path.expanduser("nsacfg.ini")

print("Добро пожаловать в оболочку NSA версии Alpha 0.0.4!")

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def reboot():
        os.system("clear")
        os.execv(sys.executable, [sys.executable] + sys.argv)

def sound():
    volume_str = input("Укажите нужное значение громкости звука:")
    volume  = int(volume_str)
    mix = alsaaudio.Mixer()
    current_volume = mix.getvolume()[0]
    if 0 <= volume <= 100:
        mix.setvolume(volume)
        cprint("Громкость была успешно изменена!", "light_green")
    else:
        cprint("ОШИБКА:не удалось изменить звук, возможно вы ввели неверное значение.", "red")

def help1():
    cprint("Доступные команды:", "light_green")
    cprint("ред - редактировать файл при помощи vim", "green")
    cprint("калькулятор - bc", "green")
    cprint("часы - date", "green")
    cprint("кат - ls", "green")
    cprint("календарь", "green")
    cprint("созкат - создать каталог", "green")
    cprint("написать - вывести текст на экран", "green")
    cprint("трк - текущий рабочий каталог", "green")
    cprint("см - cat", "green")
    cprint("сд - сменить директорию", "green")
    cprint("прм - переместить файл/каталог", "green")
    cprint("удл - удалить файл/каталог", "green")
    cprint("установить - установить указанный пакет", "green")
    cprint("удалить - удалить указанный пакет", "green")
    cprint("обновить - установка обновлений", "green")
    cprint("воиспроизвести - воиспроизвести видео при помощи mpv (планируется переработка этой функции)", "green")
    cprint("скриншот - делает скриншот через scrot", "green")
    cprint("помощь - вызвать помощь", "green")
    cprint("выход - выйти из оболочки", "green")
    cprint("питон - python", "green")
    cprint("перезапуск - перезапустить скрипт", "green")

def PMinstall(package_name,distro):
    if distro == "Debian":
        subprocess.run(["sudo", "apt", "install", package_name])
    elif distro == "Fedora":
        subprocess.run(["sudo", "dnf", "install", package_name])
    elif distro == "OpenSUSE":
        subprocess.run(["sudo", "zypper", "install", package_name])
    elif distro == "Arch":
        subprocess.run(["sudo", "pacman", "-S", package_name])
    elif distro == "Void":
        subprocess.run(["sudo", "xbps-install", "-y", package_name])
    elif distro == "Gentoo":
        subprocess.run(["sudo", "emerge", package_name])
    elif distro == "FreeBSD":
        subprocess.run(["sudo", "pkg", "install", package_name])
    elif distro == "OpenBSD":
        subprocess.run(["doas", "pkg_add", package_name])
    elif distro == "NetBSD":
        subprocess.run(["doas", "pkgin", "install", package_name])
    elif distro == "LFS":
        print("похоже вам придётся компилировать все программы вручную ;)")
        print("но если LFS всё же не ваш дистрибутив... измените строку distro в nsacfg.ini")
    else:
        print("Ваш дистрибутив не поддерживается.")

def PMremove(package_name,distro):
    if distro == "Debian":
        subprocess.run(["sudo", "apt", "remove", package_name])
    elif distro == "Fedora":
        subprocess.run(["sudo", "dnf", "remove", package_name])
    elif distro == "OpenSUSE":
        subprocess.run(["sudo", "zypper", "remove", package_name])
    elif distro == "Arch":
        subprocess.run(["sudo", "pacman", "-Rcs", package_name])
    elif distro == "Void":
        subprocess.run(["sudo", "xbps-remove", package_name])
    elif distro == "Gentoo":
        subprocess.run(["sudo", "emerge", "--unemerge", package_name])
    elif distro == "FreeBSD":
        subprocess.run(["sudo", "pkg", "delete", package_name])
    elif distro == "OpenBSD":
        subprocess.run(["doas", "pkg_delete", package_name])
    elif distro == "NetBSD":
        subprocess.run(["doas", "pkgin" "remove", package_name])
    else:
        print("Ваш дистрибутив не поддерживается.")

def PMupdate(package_name, distro):
    if distro == "Debian":
        subprocess.run(["sudo", "apt", "update", package_name])
    elif distro == "Fedora":
        subprocess.run(["sudo", "dnf", "update", package_name])
    elif distro == "OpenSUSE":
        subprocess.run(["sudo", "zypper", "up", package_name])
    elif distro == "Arch":
        subprocess.run(["sudo", "pacman" "-Syu", package_name])
    elif distro == "Void":
        subprocess.run(["sudo", "xbps-install", "-Su", package_name])
    elif distro == "Gentoo":
        subprocess.run(["sudo", "emerge" "-avuDN", package_name])
    elif distro == "FreeBSD":
        subprocess.run("sudo", "pkg", "update", package_name)
    elif distro == "OpenBSD":
        subprocess.run(["doas", "pkg_update", "-u", package_name])
    elif distro == "NetBSD":
        subprocess.run(["doas", "pkgin", "update", package_name])
    else:
        print("ваш дистрибутив не поддерживается")

def PMupdate_all(distro):
    if distro == "Debian":
        subprocess.run(["sudo", "apt", "update"])
    elif distro == "Fedora":
        subprocess.run(["sudo", "dnf", "update"])
    elif distro == "OpenSUSE":
        subprocess.run(["sudo", "zypper", "up"])
    elif distro == "Arch":
        subprocess.run(["sudo", "pacman", "-Syu"])
    elif distro == "Void":
        subprocess.run(["sudo", "xbps-install", "-Su"])
    elif distro == "Gentoo":
        subprocess.run(["sudo" "emerge", "-avuDN", "@world"])
    elif distro == "FreeBSD":
        subprocess.run(["sudo", "pkg", "update"]) 
    elif distro == "OpenBSD":
        subprocess.run(["doas" "pkg_update", "-u"]) 
    elif distro == "NetBSD":
        subprocess.run(["doas", "pkgin", "update"])
    else:
        print("Ваш дистрибутив не поддерживается.")

команды = {
    "ред": "vim",
    "калькулятор": "bc",
    "часы": "date",
    "кат": "ls --color=auto",
    "неофетч": "neofetch",
    "написать": "echo",
    "выход": "exit",
    "созкат": "mkdir",
    "создать": "touch",
    "очистить": "clear",
    "сд": "cd",
    "см": "cat",
    "трк": "pwd",
    "удл": "rm",
    "прм": "mv",
    "календарь": "cal",
    "воиспроизвести": "mpv",
    "питон": "python",
    "память": "free -m",
    "аптайм": "uptime -p",
    "скриншот": "scrot",
}
command_list = list(команды.keys()) + ["выход","сд","установить","удалить","обновить","перезапуск"] 

def completer(text, state):
    options = [x for x in command_list if x.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

config = load_config()
if 'settings' not in config:
    config['settings'] = {}

distro = config['settings'].get('distro')

if not distro:
    distro = input("Какой дистрибутив вы используете?: ")
    config['settings']['distro'] = distro
    save_config(config)

while True:
    пользователь = getpass.getuser()
    cwd2 = os.getcwd()
    строка = f"{пользователь}@{cwd2}> " 
    try:
        вса = input(строка)
    except EOFError:
        print("nExiting...")
        break
    except KeyboardInterrupt:
        print("nInterrupting...")
        continue

    parts = вса.split()
    command = parts[0]
    argument = ""

    if len(parts) > 1:
        argument = " ".join(parts[1:])

    if command == "выход":
        exit()
    elif command == "сд":
        try:
            os.chdir(argument)
        except FileNotFoundError:
            print(f"Директория '{argument}' не найдена.")
        except NotADirectoryError:
            print(f"'{argument}' не является директорией.")
        except OSError as e:
            print(f"Ошибка: {e}")
    elif command == "перезапуск":
        reboot()
    elif command == "звук":
        sound()
    elif command == "помощь":
        help1()
    elif command == "обновить":
        if argument:
            PMupdate(argument, distro)
        else:
            PMupdate_all(distro)
    elif command == "удалить":
        if argument:
            PMremove(argument, distro)
        else:
            print("Укажите имя пакета для удаления.")
    elif command == "установить":
        if argument:
             PMinstall(argument,distro) 
        else:
            print("Укажите имя пакета для установки.")
    elif command in команды:
        command_to_execute = команды[command]
        full_command = command_to_execute
        if argument:
            full_command = f'{command_to_execute} {argument}'
        os.system(full_command)
    else:
        print("Неизвестная команда")

import os
import getpass
import readline
import subprocess
import rlcompleter
import configparser 

CONFIG_FILE = os.path.expanduser("nsacfg.ini")

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def PMinstall(package_name,distro):
    if distro == "Debian":
        subprocess.run(["sudo", "apt", "install", package_name])
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
    elif distro == "Arch":
        subprocess.run(["sudo", "pacman", "-Syu"])
    elif distro == "Void":
        subprocess.run(["sudo", "xbps-install", "-Su"])
    elif distro == "Gentoo":
        subprocess.run(["sudo" "emerge", "-avuDN", "@world"])
    elif distro == "FreeBSD":
        subprocess.run(["sudo", "pkg", "update"]) # не забудь потом доделать PMupdate а также добавить поддержку Fedora, OpenSUSE, Mint (и других debian based дистрибутивов)
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
}

command_list = list(команды.keys()) + ["выход","сд","установить","удалить","обновить"] 

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

import os
import getpass
import readline
import rlcompleter

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
    "воиспроизвести": "mpv"
}

command_list = list(команды.keys()) + ["выход", "сд"] 


def completer(text, state):
    """Функция для автодополнения."""
    options = [x for x in command_list if x.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

while True:
    пользователь = getpass.getuser()
    cwd2 = os.getcwd()
    строка = f"{пользователь}@{cwd2}> "
    try:
        вса = input(строка)
    except EOFError:
        print("\nExiting...")
        break
    except KeyboardInterrupt:
        print("\nInterrupting...")
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
    elif command in команды:
        command_to_execute = команды[command]
        full_command = command_to_execute
        if argument:
            full_command = f'{command_to_execute} {argument}'
        os.system(full_command)
    else:
        print("Неизвестная команда")

import inspect
import os
from pathlib import Path
from shutil import copyfile

from sty import fg


# Static Functions #
def file_exists(path):
    return Path(path).is_file()


def folder_exists(path):
    return Path(path).is_dir()


def read_file(path):
    if not file_exists(path):
        return None
    file = open(path, "r")
    data = file.read()
    file.close()
    return data


# Credit to: https://stackoverflow.com/a/684344/5216257
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


# Credit to: https://stackoverflow.com/a/543375/5216257
def stop_program():
    raise SystemExit(0)


# TODO: Test backup function
def overwrite_file(path, data):
    # Back up changes before committing them
    p = Path(path)
    if p.exists():
        copyfile(path, f"{path}.old")
        log(f"Created a backup of: {path}")

    # Create or overwrite file
    file = open(path, "w")
    file.seek(0)
    file.write(data)
    file.truncate()
    file.close()
    log(f"Wrote data to: {path}")


# Setup a means for creating more readable log output.
LEVEL_ERROR = -2
LEVEL_WARN = -1
LEVEL_NORMAL = 0
LEVEL_OK = 1


def log(message, level=LEVEL_NORMAL):
    stack = inspect.stack()
    def_name = stack[1].__getattribute__("function")
    line_number = stack[1].__getattribute__("lineno")
    filename = str(stack[1].__getattribute__("filename"))
    filename = filename[filename.rindex('/'):]

    source = ""
    if def_name == "<module>" and len(stack) == 2:
        # 0/2 parents; directly executed code without a class or (class-less) function; a.k.a raw file-code
        source = f"(emancipated) {filename}"
    elif len(stack) == 3:
        # 1/2 parents; either run directly from class or from (class-less) function
        source = f"(divorced) {filename} -> {def_name}()"
    elif len(stack) >= 4:
        # 2/2 parents; both class and method present; a.k.a class-method
        class_name = stack[2].__getattribute__("function")
        source = f"{class_name}.{def_name}()"

    source = f"{source} @ line {line_number}"

    color = {
        LEVEL_ERROR: f"{fg.red}[ERROR]",
        LEVEL_WARN: f"{fg.li_yellow}[WARN]",
        LEVEL_NORMAL: "[INFO]",
        LEVEL_OK: f"{fg.da_green}[OK]"
    }
    print(f"{color.get(level)} {source} | {message}", end=f'{fg.rs}\n')

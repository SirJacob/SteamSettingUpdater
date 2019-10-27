from sty import fg
from pathlib import Path
import inspect


# Static Functions #
def file_exists(path):
    return Path(path).is_file()


def folder_exists(path):
    return Path(path).is_dir()


def read_file(path):
    file = open(path, "r")
    data = file.read()
    file.close()
    return data


# TODO: Consider backing up changes before committing them
def overwrite_file(path, data):
    file = open(path, "r")
    file.seek(0)
    file.write(data)
    file.truncate()
    file.close()


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

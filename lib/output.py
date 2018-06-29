import time
import getpass

try:
    raw_input
except:
    raw_input = input


def set_color(string, level=None):
    """
    set the string color
    """
    color_levels = {
        10: "\033[36m{}\033[0m",
        20: "\033[32m{}\033[0m",
        30: "\033[33m{}\033[0m",
        40: "\033[1m\033[31m{}\033[0m",
        50: "\033[7;31;31m{}\033[0m"
    }
    if level is None:
        return color_levels[20].format(string)
    else:
        return color_levels[int(level)].format(string)


def info(string):
    print(
        "[{}][{}] {}".format(
            set_color(time.strftime("%H:%M:%S")),
            set_color("INFO"),
            string
        )
    )


def debug(string):
    print(
        "[{}][{}] {}".format(
            set_color(time.strftime("%H:%M:%S"), level=10),
            set_color("DEBUG", level=10),
            string
        )
    )


def warning(string):
    print(
        "[{}][{}] {}".format(
            set_color(time.strftime("%H:%M:%S"), level=30),
            set_color("WARNING", level=30),
            string
        )
    )


def error(string):
    print(
        "[{}][{}] {}".format(
            set_color(time.strftime("%H:%M:%S"), level=40),
            set_color("FATAL", level=40),
            string
        )
    )


def fatal(string):
    print(
        "[{}][{}] {}".format(
            set_color(time.strftime("%H:%M:%S"), level=50),
            set_color("FATAL", level=50),
            string
        )
    )


def prompt(string, hide=False):
    if not hide:
        prompter = raw_input
    else:
        prompter = getpass.getpass
    data = prompter(
        "[{}][{}] {}".format(
            time.strftime("%H:%M:%S"), "PROMPT", string
        )
    )
    return data